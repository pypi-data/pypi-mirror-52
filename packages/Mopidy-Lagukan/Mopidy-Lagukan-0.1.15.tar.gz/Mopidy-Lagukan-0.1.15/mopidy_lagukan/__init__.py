from __future__ import unicode_literals

import logging
import os

from mopidy import config, ext


__version__ = '0.1.15'

logger = logging.getLogger(__name__)

class Extension(ext.Extension):

    dist_name = 'Mopidy-Lagukan'
    ext_name = 'lagukan'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['token'] = config.Secret()
        return schema

    def setup(self, registry):
        # You will typically only implement one of the following things
        # in a single extension.

        # TODO: Edit or remove entirely
        from .frontend import LagukanFrontend
        registry.add('frontend', LagukanFrontend)

        ## TODO: Edit or remove entirely
        #from .backend import FoobarBackend
        #registry.add('backend', FoobarBackend)

        ## TODO: Edit or remove entirely
        #registry.add('http:static', {
        #    'name': self.ext_name,
        #    'path': os.path.join(os.path.dirname(__file__), 'static'),
        #})

    def get_command(self):
        from .commands import LagukanCommand
        return LagukanCommand()
