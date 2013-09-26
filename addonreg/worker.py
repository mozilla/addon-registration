import os

from celery import Celery
from celery.signals import worker_init
from pyramid.paster import bootstrap


@worker_init.connect
def bootstrap_pyramid(signal, sender):
    # We need this so that tasks are able to access what's defined in the
    # pyramid configuration.
    config = os.environ['CONFIG']
    sender.app.settings = bootstrap(config)['registry'].settings


celery = Celery('addonreg.worker')

# These should come from the normal .ini file.
# Use Konfig here.
celery.conf.update(
    BROKER_URL="redis://localhost:6379/0",
    CELERY_IMPORTS=['addonreg.tasks'])

if __name__ == '__main__':
    celery.start()
