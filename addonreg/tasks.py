from addonreg.worker import celery


@celery.task
def record_new_hash(addon_id, sha256):
    # Find a way to get back the DB backend here (from pyramid)
    print addon_id, sha256
