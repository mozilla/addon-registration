class RawSQLBackend(object):
    """A backend using RAW SQL queries to go faster."""

    def __init__(self, config):
        self.config = config

    def hash_exists(self, addon_id, hash_):
        pass

    def register_hash(self, addon_id, hash_):
        pass
