VERSION = '0.1'

import os

from pyramid.config import Configurator
from pyramid.events import NewRequest

from konfig import Config


def get_config(filename=None):
    filename = filename or os.environ.get('CONFIG', 'development.ini')
    return Config(filename)


def setup_configuration(settings):
    config = Configurator(settings=settings)
    backend_class = config.maybe_dotted(settings['addonreg.backend'])
    backend = backend_class(config)

    def _add_backend_to_request(event):
        event.request.backend = backend

    # Attach the backend to each request and put it in the registry.
    config.add_subscriber(_add_backend_to_request, NewRequest)
    config.registry.backend = backend
    return config


def main(global_config, **settings):
    config = setup_configuration(settings)

    config.include('cornice')
    config.scan('addonreg.views')

    return config.make_wsgi_app()
