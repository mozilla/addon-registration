from celery.app import app_or_default

from addonreg.worker import celery


@celery.task
def record_new_hash(addon_id, sha256):
    app = app_or_default()
    app.registry.backend.register_hash(addon_id, sha256)
