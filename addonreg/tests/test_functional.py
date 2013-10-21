import os

from unittest2 import TestCase
import webtest


HERE = os.path.dirname(os.path.abspath(__file__))


class FunctionalTest(TestCase):

    def setUp(self):
        self.app = webtest.TestApp("config:tests.ini", relative_to=HERE)
        self.backend = self.app.app.registry.backend

    def tearDown(self):
        self.backend.empty()

    def test_get_registered_addon(self):
        addon_id = 'id@example.com'
        hash_ = '0c27ec47b62e20a20a563aaada9dfa663d76a76f'

        self.backend.register_hash(addon_id, hash_)

        data = {'id': addon_id, 'sha256': hash_}
        resp = self.app.post_json('/addon', data)

        self.assertDictEqual(resp.json, {'registered': True,
                                         'sha256': hash_,
                                         'id': addon_id})

    def test_get_unregistered_addon(self):
        addon_id = 'id@example.com'
        hash_ = '0c27ec47b62e20a20a563aaada9dfa663d76a76f'

        data = {'id': addon_id, 'sha256': hash_}
        resp = self.app.post_json('/addon', data)

        self.assertDictEqual(resp.json, {'registered': False,
                                         'sha256': hash_,
                                         'id': addon_id})

    def test_new_hash_submission(self):
        addon_id = 'id@example.com'
        hash_ = '0c27ec47b62e20a20a563aaada9dfa663d76a76f'

        data = {'id': addon_id, 'sha256': hash_}
        self.app.post_json('/hash', data, status=202)
        self.assertTrue(self.backend.hash_exists(addon_id, hash_))

    def test_get_multiple_hashes(self):

        # Register two hashes in the db.
        addons_ids = ['id@example.com', 'id2@example.com']
        hashes = ['0c27ec4762e20a20a563aaada9dfa663d76a76f',
                  '123afe1262e20a20a563aaada9d123af1231af2']

        for data in zip(addons_ids, hashes):
            self.backend.register_hash(*data)

        # Describe an addon that's not registered.
        addons_ids.append('unregistered')
        hashes.append('123afe1262e20a20a563aaada9d123af1231af2')

        addons_list = [{'id': idx, 'sha256': sha}
                       for (idx, sha) in zip(addons_ids, hashes)]

        data = {'addons':  addons_list}
        resp = self.app.post_json('/addons', data)

        addons = resp.json['addons']
        for idx in range(2):
            self.assertDictEqual(addons[idx], {u'registered': True,
                                               u'sha256': hashes[idx],
                                               u'id': addons_ids[idx]})

        self.assertDictEqual(addons[2], {u'registered': False,
                                         u'sha256': hashes[2],
                                         u'id': addons_ids[2]})
