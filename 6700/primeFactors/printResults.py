'''
Created on Jul 25, 2014

@author: susanha
'''
import GitFile
import Transformations
import Commit
import codecs

class Results:
    
    def __init__(self):
        self.totalCommits = 0
        self.totalTransformations = 0
        self.totalAntiTransformations = 0
        self.totalLinesOfCode = 0
        self.totalSubmissions = 0
    
    def printResults(self, fileName):
        myTransNames = Transformations.Trans()
        myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700Fall14\\Assignment1\\"+fileName)
        self.totalSubmissions = self.totalSubmissions + 1
        myGitFile.readGitFile()
        myFiles = myGitFile.getFiles()
        myCommits = myGitFile.getCommits()
        addedLines = 0
        nbrTransformations = 0
        nbrAntiTransformations = 0
        outFile = open("c:\\Users\\susanha\\git\\6700Fall14\\Assignment1\\"+fileName+".gitout", "w")
        outFile.write( "Commits in log file:  " + str(len(myCommits)))
        nbrOfCommits = len(myCommits)
        self.totalCommits = self.totalCommits + nbrOfCommits
        for myCommit in myCommits:
            outFile.write("\r\nCommit Number:"+ str(myCommit.commitNbr) + "  Added lines:" + str(myCommit.addedLinesInCommit) +
                ".  Deleted lines:" + str(myCommit.deletedLinesInCommit) + ".  Test files:" + str(myCommit.testFiles) + 
                ".  Production files:" + str(myCommit.prodFiles) + ".  Number of Transformations:  "+ str(myCommit.numberOfTransformations)+". \n\r")
            addedLines = addedLines + myCommit.addedLinesInCommit
            myTrans = myCommit.getTransformations()
            outFile.write("Transformations:")
            for myTran in myTrans:
                outFile.write("\r" + myTransNames.myName(myTran))
                if myTran > 0:
                    nbrTransformations = nbrTransformations + 1
                else:
                    nbrAntiTransformations = nbrAntiTransformations + 1
        self.totalTransformations = self.totalTransformations + nbrTransformations
        self.totalAntiTransformations = self.totalAntiTransformations + nbrAntiTransformations
        self.totalLinesOfCode = self.totalLinesOfCode + addedLines
        outFile.write("\r\nFiles in logfile:  " + str(len(myFiles)) + "\r\n")
        for myFile in myFiles:
            outFile.write("\r\n" + myFile.fileName + " added in commit:" + str(myFile.commitAdded) + ".  Is a test file:" + str(myFile.testFile))
            for myCommitDetails in myFile.commitDetails:
                outFile.write("\r\nCommit " + str(myCommitDetails.commitNbr) + ".  Added lines:" + str(myCommitDetails.addedLines) + ".  Deleted lines:" + str(myCommitDetails.deletedLines))
                outFile.write("\r\nMethods added/modified:" )
                for myMethodName in myCommitDetails.methodNames:
                    outFile.write("\r" + myMethodName)
                
        outFile.close()
        return addedLines/nbrOfCommits, nbrTransformations/nbrOfCommits
    