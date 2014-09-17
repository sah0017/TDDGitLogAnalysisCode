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
        pass
    
    def printResults(self, fileName):
        myTransNames = Transformations.Trans()
        myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700Fall14\\Assignment1\\"+fileName)
        myGitFile.readGitFile()
        myFiles = myGitFile.getFiles()
        myCommits = myGitFile.getCommits()
        outFile = open("c:\\Users\\susanha\\git\\6700Fall14\\Assignment1\\"+fileName+".gitout", "w")
        outFile.write( "Commits in log file:  " + str(len(myCommits)))
        for myCommit in myCommits:
            outFile.write("\r\nCommit Number:"+ str(myCommit.commitNbr) + "  Added lines:" + str(myCommit.addedLinesInCommit) +
                ".  Deleted lines:" + str(myCommit.deletedLinesInCommit) + ".  Test files:" + str(myCommit.testFiles) + ".  Production files:" + str(myCommit.prodFiles) + ".\n\r")
            myTrans = myCommit.getTransformations()
            outFile.write("Transformations:")
            for myTran in myTrans:
                outFile.write("\r" + myTransNames.myName(myTran))
        outFile.write("\r\nFiles in logfile:  " + str(len(myFiles)) + "\r\n")
        for myFile in myFiles:
            outFile.write("\r\n" + myFile.fileName + " added in commit:" + str(myFile.commitAdded) + ".  Is a test file:" + str(myFile.testFile))
            for myCommitDetails in myFile.commitDetails:
                outFile.write("\r\nCommit " + str(myCommitDetails.commitNbr) + ".  Added lines:" + str(myCommitDetails.addedLines) + ".  Deleted lines:" + str(myCommitDetails.deletedLines))
                outFile.write("Methods added/modified:" )
                for myMethodName in myCommitDetails.methodNames:
                    outFile.write("\r" + myMethodName)
        outFile.close()
        
    