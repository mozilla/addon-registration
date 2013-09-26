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


celery = Celery()
celery.config_from_object('celeryconfig')

if __name__ == '__main__':
    celery.start()
