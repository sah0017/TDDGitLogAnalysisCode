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
        myTransformations = []
        self.myGitFile.readGitFile("c:\\Users\\susanha\\git\\6700test\\revLogFile-short")
        self.assertEqual(self.myGitFile.getTransformations(),['New line', 'line removed', self.myTrans.NULL,'New line'])
        
    def testGitFileCommits(self):
        myCommits = []
        self.myGitFile.readGitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
        self.assertEqual(len(self.myGitFile.getCommits()), 7)
    ''' 
    def testGitFileCommitsLOC(self):
        myCommits = []
        self.myGitFile.readGitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
        myCommits = self.myGitFile.getCommits()
        self.assertEqual((myCommits[1]), 7)
    '''         
    def testGitFiles(self):
        myFiles = []
        self.myGitFile.readGitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
        self.assertEqual(len(self.myGitFile.getFiles()),4)

    def testGitFileNames(self):
        myFiles = []
        self.myGitFile.readGitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
        myFiles = self.myGitFile.getFiles()
        self.assertEqual(myFiles[0].getFileName(),'testPrimeFactor.py')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGitFile1']
    unittest.main()