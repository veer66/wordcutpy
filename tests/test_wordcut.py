import unittest
import sys
import os
sys.path.append(os.path.abspath('..'))
from wordcut import Wordcut

class TestWordcut(unittest.TestCase):
    def setUp(self):
        self.wordcut = Wordcut.bigthai()
        
    def test_empty_input(self):
        self.assertEqual(self.wordcut.tokenize(""),[])

    def test_none_input(self):
        self.assertEqual(self.wordcut.tokenize(None),[])

    def test_simple_one(self):
        self.assertEqual(self.wordcut.tokenize("ฉันกิน"),
                         ["ฉัน", "กิน"])
