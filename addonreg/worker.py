import os

from celery import Celery
from celery.app import app_or_default
from celery.signals import worker_process_init
from pyramid.paster import bootstrap

from addonreg import get_config


@worker_process_init.connect
def bootstrap_pyramid(signal, sender):
    # We need this so that tasks are able to access what's defined in the
    # pyramid configuration.
    config = os.environ['CONFIG']
    app = app_or_default()
    app.registry = bootstrap(config)['registry']


celery = Celery('addonreg.worker')

# These should come from the normal .ini file.
# Use Konfig here.
config = get_config()
celery.conf.update(
    BROKER_URL=config.get('app:main', 'celery.broker'),
    CELERY_IMPORTS=['addonreg.tasks'])

if __name__ == '__main__':
    celery.start()
