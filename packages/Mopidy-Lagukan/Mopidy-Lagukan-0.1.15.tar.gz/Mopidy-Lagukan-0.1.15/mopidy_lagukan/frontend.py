from __future__ import print_function

import pykka

from mopidy import core, httpclient
import cPickle as pickle
import edn_format
import appdirs
import os
import time
import uuid
import requests
import json
import logging
import time
from frozendict import frozendict

logger = logging.getLogger(__name__)

# todo send collection in (rate-limited) batches
# todo handle invalid client id

auth_url = "https://securetoken.googleapis.com/v1/token?key=AIzaSyCMIaf1mHHyJziOI0xRw0Qgw6Bh5f5UUS8"
backend_url = "https://79gcws2i5i.execute-api.us-east-1.amazonaws.com/dev"
#backend_url = "http://localhost:8080"
streaming_sources = {'spotify'}
source_uris = {'local:directory', 'spotifyweb:yourmusic:songs', 'gmusic:track'}
state_file = os.path.join(appdirs.user_data_dir(), 'mopidy-lagukan', 'state')
unrecognized_file = os.path.join(appdirs.user_data_dir(), 'mopidy-lagukan', 'unrecognized')

def get_session(config):
    proxy = httpclient.format_proxy(config['proxy'])
    user_agent = httpclient.format_user_agent('Mopidy-Lagukan/0.1.6')

    session = requests.Session()
    session.proxies.update({'http': proxy, 'https': proxy})
    session.headers.update({'user-agent': user_agent})

    return session

def select_keys(d, keys):
    return {k: d[k] for k in keys if k in d}

def collect(library, uri):
    ret = []
    for ref in library.browse(uri).get():
        if ref.type == 'directory':
            ret.extend(collect(library, ref.uri))
        elif ref.type == 'track':
            ret.append(ref.uri)
    return ret

def format_track(track):
    ret = {}
    if track.name is not None:
        ret['track/title'] = track.name
    if len(track.artists) != 0:
        ret['track/artists'] = [artist.name for artist in track.artists]
    elif track.album != None and len(track.album.artists) != 0:
        ret['track/artists'] = [artist.name for artist in track.album.artists]
    return ret

def read_state():
    with open(state_file, 'r') as f:
        return pickle.load(f)

def write_state(s):
    try:
        os.makedirs(os.path.dirname(state_file))
    except:
        pass
    with open(state_file, 'w') as f:
        pickle.dump(select_keys(s, ['client-id', 'blacklist', 'last-init']), f, pickle.HIGHEST_PROTOCOL)

def debug(local):
    import code
    import sys
    params = globals().copy()
    params.update(local)
    code.interact(local=params)
    sys.exit(0)

class LagukanFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(LagukanFrontend, self).__init__()
        self.core = core
        self.config = config
        self.session = get_session(config)
        self.expire_time = None

        # TODO check blacklist

        try:
            state = read_state()
        except:
            state = {'client-id': uuid.UUID(self.hit('/register-client')['client-id'])}
            write_state(state)
        self.client_id = state['client-id']
        last_init = state.get('last-init')

        if not last_init or last_init < time.time() - 60 * 60 * 24 * 3:
            track_uris = []
            for uri in source_uris:
                track_uris.extend(set(collect(core.library, uri)))

            logger.info("Collecting library info for Lagukan...")
            tracks = [track
                      for result in core.library.lookup(uris=track_uris).get().values()
                      for track in result]
            unrecognized = []
            collection = []
            for t in tracks:
                ft = format_track(t)
                if 'track/artists' in ft:
                    ft['track/artists'] = tuple(ft['track/artists'])
                    ft = frozendict(ft)
                    collection.append(ft)
                else:
                    unrecognized.append(t)

            new_collection = []
            for ft in set(collection):
                ft = dict(ft)
                ft['track/artists'] = list(ft['track/artists'])
                new_collection.append(ft)
            collection = new_collection

            if len(unrecognized) > 0:
                with open(unrecognized_file, 'w') as f:
                    for t in unrecognized:
                        print(t.uri.replace("%20", " "), format_track(t), file=f)
                logger.info("There were " + str(len(unrecognized)) + " tracks without either "
                    + "title or artist metadata. These tracks will not be played by Lagukan. "
                    + "See " + unrecognized_file + " to see the tracks.")

            payload = {'client-id': self.client_id,
                       'collection': collection}
            self.hit('/init', payload)

            state['last-init'] = time.time()
            write_state(state)

        self.recommend()

    def recommend(self, event=None):
        sources = [k for k in self.config.keys()
                     if k in streaming_sources and self.config[k]['enabled']]
        payload = {'client-id': self.client_id, 'event': event, 'sources': sources}
        metas = self.hit('/recommend', payload)['recommendations']

        tracks, not_found = self.get_tracks(metas)
        self.core.tracklist.replace_queue(tracks)

        if len(not_found) > 0:
            state = read_state()
            if 'blacklist' not in state:
                state['blacklist'] = []
            state['blacklist'].extend(not_found)
            write_state(state)
            self.hit('/blacklist', {'client-id': self.client_id, 'blacklist': not_found})

    def hit(self, url, payload=None):
        start = time.time()
        if url == '/register-client':
            logger.info("Registering with Lagukan")
        elif url == '/init':
            logger.info("Sending library info to Lagukan")
        elif url == '/recommend':
            logger.info("Getting recommendations from Lagukan...")
        self.update_token()

        url = backend_url + url
        payload = edn_format.dumps(payload, keyword_keys=True)
        headers = {'Authorization': 'Bearer ' + self.token,
                   'Content-Type': 'application/edn',
                   'Accept': 'application/json'}

        response = self.session.post(url, data=payload, headers=headers)
        end = time.time()
        #logger.info("done (" + str(int(end - start)) + " seconds)")
        if not response.ok:
            logger.error(response.text)
        #import code; code.interact(local=locals())
        response.raise_for_status()
        if url == '/recommend':
            logger.info("Done getting recommendations from Lagukan")
        return json.loads(response.text)

    def update_token(self):
        if not self.expire_time or self.expire_time < time.time() + 60 * 10:
            response = self.session.post(auth_url,
                    {'grant_type': 'refresh_token', 'refresh_token': self.config['lagukan']['token']},
                    headers={'Cache-Control': 'no-cache', 'Origin': 'https://lagukan.com'}).json()
            self.token = response['access_token']
            self.expire_time = time.time() + int(response['expires_in'])

    def track_playback_ended(self, tl_track, time_position):
        try:
            event = {'event.track-end/track': format_track(tl_track.track),
                     'event.track-end/length': tl_track.track.length,
                     'event.track-end/position': time_position}
        except:
            event = None
        self.recommend(event)

    def get_tracks(self, metas):
        tracks = []
        not_found = []
        for meta in metas:
            meta.pop('album', None)
            query = {}
            for k, qk in zip(['track/artists', 'track/title'],
                             ['artist', 'track_name']):
                if k in meta:
                    val = meta[k]
                    if k != 'track/artists':
                        val = [val]
                    query[qk] = val
            for source in ['local', 'spotify', 'gmusic']:
                result = self.core.library.search(query, uris=[source + ':'], exact=True).get()
                result = [t for r in result
                            for t in r.tracks
                            if format_track(t) == meta]
                if len(result) > 0:
                    break
            if len(result) > 0:
                tracks.append(result[0])
            else:
                not_found.append(meta)
        return tracks, not_found
