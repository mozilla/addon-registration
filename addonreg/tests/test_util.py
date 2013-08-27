from unittest import TestCase
import os.path

from addonreg import util

HERE = os.path.dirname(os.path.abspath(__file__))


class TestUtil(TestCase):

    def test_get_file_hash(self):
        filename = os.path.join(HERE, 'testfile.xpi')
        self.assertEquals('55204f54f8711ef1041428c286f475b3',
                          util.get_file_hash(filename))
