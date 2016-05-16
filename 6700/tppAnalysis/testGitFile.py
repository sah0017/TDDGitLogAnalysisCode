'''
Created on Jul 10, 2014

@author: susanha
'''
import unittest
import GitFile
import Transformations
import Commit
import PyFile
import PyFileCommitDetails

class Test(unittest.TestCase):

    def setUp(self):
        self.myTrans = Transformations.Trans()

    def testOneCommitGitFile(self):
        myTransformations = []
        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogFile-short")
        self.myGitFile.analyzeGitLogFile()
        self.assertEqual(self.myGitFile.get_transformations(),[self.myTrans.NEWFILE,self.myTrans.NULL])
        
    def testGitFileCommits(self):
        myCommits = []
        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
        self.myGitFile.analyzeGitLogFile()
        self.assertEqual(len(self.myGitFile.getCommits()), 9)
     
    def testGitFileCommitsLOC(self):
        myCommits = []
        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
        self.myGitFile.analyzeGitLogFile()
        myCommits = self.myGitFile.getCommits()
        self.assertEqual((myCommits[1].get_added_lines_in_commit()), 14)
             
    def testGitFiles(self):
        myFiles = []
        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
        self.myGitFile.analyzeGitLogFile()
        self.assertEqual(len(self.myGitFile.getFiles()),4)

    def testGitFileNames(self):
        myFiles = []
        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
        self.myGitFile.analyzeGitLogFile()
        myFiles = self.myGitFile.getFiles()
        self.assertEqual(myFiles[0].extractFileName(),'testPrimeFactor.py')

    def testFileObject(self):
        myFile = PyFile.PyFile("testname.py",True,1)
        self.assertEqual(myFile.fileName, "testname.py")
        
    def testFileObjectLinesPerCommit(self):
        myCommitList = []
        myFile = PyFile.PyFile("testname2.py",True,2)
        myFile.setCommitDetails(1,16,0)
        myTestCommits = myFile.getCommitDetails()
        self.assertEqual(myTestCommits[0].getCommitDetails(), [1,16,0])

    def testCommitDetails(self):
        myFiles = []
        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
        self.myGitFile.analyzeGitLogFile()
        myFiles = self.myGitFile.getFiles()
        myCommitDetails = myFiles[0].getCommitDetails()
        self.assertEqual(myCommitDetails[0].getCommitDetails(),[1,18,0])
        self.assertEqual(myCommitDetails[1].getCommitDetails(), [2,2,1])
        self.assertEqual(myCommitDetails[2].getCommitDetails(), [3,2,0])
        
    def testCommitTransformations(self):
        myCommit = Commit.Commit(1,14,4,1,1)
        myCommit.addTransformation(1)
        self.assertEqual(myCommit.get_transformations(), [1])

    def testCommitTransformationsInShortGitFile(self):

        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogFile-short")
        self.myGitFile.analyzeGitLogFile()
        myCommits = self.myGitFile.getCommits()
        self.assertEqual(myCommits[0].get_transformations(),[self.myTrans.NEWFILE,self.myTrans.NULL])

    def testCommitTransformationsInLongGitFile(self):

        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogFile")
        self.myGitFile.analyzeGitLogFile()
        myCommits = self.myGitFile.getCommits()
        self.assertEqual(myCommits[0].get_transformations(),[self.myTrans.NEWFILE,self.myTrans.NULL])
        self.assertEqual(myCommits[1].get_transformations(), [self.myTrans.NEWFILE,self.myTrans.ConstOnly])
        self.assertEqual(myCommits[2].get_transformations(), [self.myTrans.SF,self.myTrans.C2V])
        self.assertEqual(myCommits[3].get_transformations(), [self.myTrans.SF,self.myTrans.SF])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGitFile1']
    unittest.main()