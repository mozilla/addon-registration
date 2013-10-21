from collections import defaultdict


class PythonBackend(object):
    """A backend using python structured in memory to store data.

    This doesn't really have any value, appart from the tests.
    """

    def __init__(self, config):
        self.config = config
        self._hashs = defaultdict(list)

    def hash_exists(self, addon_id, hash_):
        return hash_ in self._hashs[addon_id]

    def hashes_exists(self, addons):
        """Returns a list of registered hashes"""
        return [info for info in addons if self.hash_exists(*info)]

    def register_hash(self, addon_id, hash_):
        if hash_ not in self._hashs[addon_id]:
            self._hashs[addon_id].append(hash_)

    def empty(self):
        """Empty the backend"""
        self._hashs = defaultdict(list)
