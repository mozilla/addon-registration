import os
from unittest2 import TestCase

from addonreg.backends.rawsql import RawSQLBackend


class TestSQLBackend(TestCase):

    # By default, the tests are using SQLite in order to be faster.
    # You can change that (if you want to run the tests against a real database
    # for instance) by changing the SQLURI environment variable.
    _SQLURI = os.environ.get('SQLURI', 'sqlite:////tmp/wimms')

    def setUp(self):
        super(TestSQLBackend, self).setUp()
        self.backend = RawSQLBackend(sqluri=self._SQLURI, create_tables=True)
        self.guids = (u'{9c51bd27-6ed8-4000-a2bf-36cb95c0c947}',
                      u'id@example.com')
        self.hashes = (u'31f7a65e315586ac198bd798b6629ce4903d0899476d5741a9f32'
                       'e2e521b6a66', u'15586ac198bd798b6629ce4903d0899476d57',
                       '41a9f3231f7a65e31')
        self._sqlite = self.backend._engine.driver == 'pysqlite'

    def tearDown(self):
        if self._sqlite:
            filename = self.backend.sqluri.split('sqlite://')[-1]
            if os.path.exists(filename):
                os.remove(filename)
        else:
            self.backend._safe_execute('drop table hashes;')

    def test_read(self):
        # Let's create a hash to test if we're able to read it back.
        self.backend._safe_execute(
            """INSERT INTO hashes (addonid, sha256, registered)
               VALUES ("%s", "%s", 1)""" % (self.guids[0], self.hashes[0]))

        self.assertTrue(self.backend.hash_exists(self.guids[0],
                                                 self.hashes[0]))
        self.assertFalse(self.backend.hash_exists(self.guids[1],
                                                  self.hashes[1]))

    def test_write(self):
        self.backend.register_hash(self.guids[0], self.hashes[0])
        self.assertTrue(self.backend.hash_exists(self.guids[0],
                        self.hashes[0]))

    def test_hashes_exists(self):
        for guid, sha in zip(self.guids, self.hashes):
            self.backend._safe_execute(
                """INSERT INTO hashes (addonid, sha256, registered)
                   VALUES ("%s", "%s", 1)""" % (guid, sha))

        resp = self.backend.hashes_exists(zip(self.guids, self.hashes))

        self.assertEquals(len(resp), 2)
        self.assertIn((self.guids[0], self.hashes[0]), resp)
        self.assertIn((self.guids[1], self.hashes[1]), resp)
