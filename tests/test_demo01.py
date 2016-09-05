import os
import sys
import unittest2 as unittest
import sure
sys.path.insert(0, os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0], 'src'))

class TestDemo01(unittest.TestCase):

    def test_ok(self):
        assert True == True
        



if __name__ == '__main__':
    unitest.main()




