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

    def test_single_unk(self):
        self.assertEqual(self.wordcut.tokenize("ฬฬฬ"),
                         ["ฬฬฬ"])

    def test_simple_roman_without_space(self):
        self.assertEqual(self.wordcut.tokenize("ฬฬROฬฬ"),
                         ["ฬฬ", "RO", "ฬฬ"])

    def test_simple_space(self):
        self.assertEqual(self.wordcut.tokenize("ฬฬ  มม"),
                         ["ฬฬ", "  ", "มม"])
