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

    def testLargeGitFile(self):
        myTransformations = []
        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogFile-short")
        self.myGitFile.readGitFile()
        self.assertEqual(self.myGitFile.getTransformations(),[self.myTrans.NULL])
        
    def testGitFileCommits(self):
        myCommits = []
        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
        self.myGitFile.readGitFile()
        self.assertEqual(len(self.myGitFile.getCommits()), 7)
     
    def testGitFileCommitsLOC(self):
        myCommits = []
        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
        self.myGitFile.readGitFile()
        myCommits = self.myGitFile.getCommits()
        self.assertEqual((myCommits[1].getAddedLinesInCommit()), 7)
             
    def testGitFiles(self):
        myFiles = []
        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
        self.myGitFile.readGitFile()
        self.assertEqual(len(self.myGitFile.getFiles()),4)

    def testGitFileNames(self):
        myFiles = []
        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
        self.myGitFile.readGitFile()
        myFiles = self.myGitFile.getFiles()
        self.assertEqual(myFiles[0].getFileName(),'testPrimeFactor.py')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGitFile1']
    unittest.main()