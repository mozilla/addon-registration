import os

from celery import Celery
from celery.signals import worker_process_init
from pyramid.paster import bootstrap

from addonreg import get_config


@worker_process_init.connect
def bootstrap_pyramid(signal, sender):
    # We need this so that tasks are able to access what's defined in the
    # pyramid configuration.
    config = os.environ['CONFIG']
    bootstrap(config)


celery = Celery('addonreg.worker')

# These should come from the normal .ini file.
# Use Konfig here.
conf = get_config()
section = conf.get_map('celery')
celery.conf.update(
    BROKER_URL=section.get('broker'),
    CELERY_IMPORTS=['addonreg.tasks'],
    CELERY_ALWAYS_EAGER=section.get('always_eager', False))


if __name__ == '__main__':
    celery.start()
