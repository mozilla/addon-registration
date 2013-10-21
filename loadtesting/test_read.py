from loads import TestCase
from hashlib import sha256

import random


def _get_hash(*data):
    h = sha256()
    h.update(*data)
    return h.hexdigest()

_DATA = [('id%s@example.com' % idx, _get_hash(idx)) for idx in range(0, 200)]


class LoadTest(TestCase):

    def test_get_registered_addon(self):
        idx, sha = random.choice(_DATA)
        data = {'id': idx, 'sha256': sha}
        resp = self.app.post_json('/addon', data)

        self.assertDictEqual(resp.json, {'registered': True,
                                         'sha256': sha,
                                         'id': idx})

    def test_get_unregistered_addon(self):
        idx = 'unexistant@example.com'
        sha = 'unregistered_addon_hash'

        data = {'id': idx, 'sha256': sha}
        resp = self.app.post_json('/addon', data)

        self.assertDictEqual(resp.json, {'registered': False,
                                         'sha256': sha,
                                         'id': idx})

    def test_get_multiple_hashes(self):
        sample = random.sample(_DATA, 10)
        addons_list = [{'id': idx, 'sha256': sha}
                       for (idx, sha) in sample]

        data = {'addons':  addons_list}
        resp = self.app.post_json('/addons', data)

        addons = resp.json['addons']
        for idx, sha in sample:
            self.assertDictEqual(addons[idx], {u'registered': True,
                                               u'sha256': sha,
                                               u'id': idx})
