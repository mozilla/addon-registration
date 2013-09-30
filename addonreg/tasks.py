from addonreg.worker import celery


@celery.task
def record_new_hash(addon_id, sha256):
    celery.registry.register_hash(addon_id, sha256)
