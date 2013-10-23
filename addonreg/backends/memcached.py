import umemcache


class MemcachedBackend(object):

    def __init__(self, config=None):
        self._client = umemcache.Client(config['memcached_server'])
        self._client.connect()

    def _key(self, *args):
        return '-'.join(args)

    def hash_exists(self, addon_id, hash_):
        try:
            registered = self._client.get(self._key(addon_id, hash_))[0]
            return registered == 'true'
        except TypeError:
            return False

    def hashes_exists(self, addons):
        keys = ['-'.join(item) for item in addons]
        resp = self._client.get_multi(keys)

        def _get_value(idx, sha):
            try:
                return resp[self._key(idx, sha)][0] == 'true'
            except TypeError:
                return False

        return [item for item in addons if _get_value(*item)]

    def register_hash(self, addon_id, hash_):
        self._client.set(self._key(addon_id, hash_), 'true')
