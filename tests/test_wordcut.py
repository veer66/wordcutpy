import unittest
import sys
import os
sys.path.append(os.path.abspath('..'))
from wordcut import Wordcut

class TestWordcut(unittest.TestCase):
    def test_empty_input(self):
        wordcut = Wordcut.bigthai()
        self.assertEqual(wordcut.tokenize(""),[])
