'''
Created on Aug 11, 2014

@author: susanha
'''
import unittest
import Fib


class Test(unittest.TestCase):


    def testFib(self):
        print (Fib.fibonacci(20))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFib']
    unittest.main()