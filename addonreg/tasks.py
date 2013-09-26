from addonreg.celery import celery


@celery.task
def record_new_hashs():
    print(celery.settings['sqlalchemy.url'])
