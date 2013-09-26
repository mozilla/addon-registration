from celery import Celery
from celery.signals import worker_init


@worker_init.connect
def bootstrap_pyramid(signal, sender):
    import os
    from pyramid.paster import bootstrap
    config = os.envion['CONFIG']
    sender.app.settings = bootstrap(config)['registry'].settings


celery = Celery()
celery.config_from_object('celeryconfig')
