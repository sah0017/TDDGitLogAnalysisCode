'''
Created on Jul 10, 2014

@author: susanha
'''
import unittest
import GitFile
import Transformations
import Commit

class Test(unittest.TestCase):

    def setUp(self):
        self.myTrans = Transformations.Trans()
        self.myGitFile = GitFile.GitFile()

    def testLargeGitFile(self):
        self.assertEqual(self.myGitFile.readGitFile("c:\\Users\\susanha\\git\\6700test\\revLogFile-short"),['New line', 'line removed', self.myTrans.NULL,'New line'])

    def testGitFileCommits(self):
        myCommits = []
        self.myGitFile.readGitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
        self.assertEqual(len(self.myGitFile.getCommits()), 0)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGitFile1']
    unittest.main()