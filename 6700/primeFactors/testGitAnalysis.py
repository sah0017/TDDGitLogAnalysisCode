'''
Created on Jul 10, 2014

@author: susanha
'''
import unittest
import GitFile
import Transformations
import Commit
import File
import CommitDetails

class Test(unittest.TestCase):

    def setUp(self):
        self.myTrans = Transformations.Trans()

    def testOneCommitGitFile(self):
        myTransformations = []
        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogFile-short")
        self.myGitFile.readGitFile()
        self.assertEqual(self.myGitFile.getTransformations(),[self.myTrans.NEWFILE,self.myTrans.NULL])
        
    def testGitFileCommits(self):
        myCommits = []
        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
        self.myGitFile.readGitFile()
        self.assertEqual(len(self.myGitFile.getCommits()), 9)
     
    def testGitFileCommitsLOC(self):
        myCommits = []
        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
        self.myGitFile.readGitFile()
        myCommits = self.myGitFile.getCommits()
        self.assertEqual((myCommits[1].getAddedLinesInCommit()), 14)
             
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

    def testFileObject(self):
        myFile = File.File("testname.py",1)
        self.assertEqual(myFile.fileName, "testname.py")
        
    def testFileObjectLinesPerCommit(self):
        myCommitList = []
        myFile = File.File("testname2.py",2)
        myFile.setCommitDetails(1,16,0)
        myTestCommits = myFile.getCommitDetails()
        self.assertEqual(myTestCommits[0].getCommitDetails(), [1,16,0])

    def testCommitDetails(self):
        myFiles = []
        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
        self.myGitFile.readGitFile()
        myFiles = self.myGitFile.getFiles()
        myCommitDetails = myFiles[0].getCommitDetails()
        self.assertEqual(myCommitDetails[0].getCommitDetails(),[1,18,0])
        self.assertEqual(myCommitDetails[1].getCommitDetails(), [2,2,1])
        self.assertEqual(myCommitDetails[2].getCommitDetails(), [3,2,0])
        
    def testCommitTransformations(self):
        myCommit = Commit.Commit(1,14,4)
        myCommit.addTransformation(1)
        self.assertEqual(myCommit.getTransformations(), [1])

    def testCommitTransformationsInGitFile(self):

        self.myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogFile-short")
        self.myGitFile.readGitFile()
        myCommits = self.myGitFile.getCommits()
        self.assertEqual(myCommits[0].getTransformations(),[self.myTrans.NEWFILE,self.myTrans.NULL])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGitFile1']
    unittest.main()