import unittest
from prefixtree import PrefixTree

class TestPrefixTree(unittest.TestCase):

    def test_basic(self):
        self.dix = [("B", "P2"),
                    ("A", "P1")]
        pt = PrefixTree(self.dix)
        
        self.assertEqual(pt.lookup(0,0,"A"),(0,True,"P1"))

    def test_longer(self):
        self.dix = [("B", "P2"),
                    ("ABC", "P1")]
        pt = PrefixTree(self.dix)
        
        self.assertEqual(pt.lookup(0,0,"A"),(0,False,None))
        self.assertEqual(pt.lookup(0,2,"C"),(0,True,"P1"))
