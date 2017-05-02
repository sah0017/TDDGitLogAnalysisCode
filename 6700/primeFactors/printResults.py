'''
Created on Jul 25, 2014

@author: susanha
'''
import GitFile
import Transformations
import Commit


if __name__ == '__main__':
    myFiles = []
    myCommits = []
    myTransNames = Transformations.Trans()
    myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\fibLog")
    myGitFile.readGitFile()
    myFiles = myGitFile.getFiles()
    myCommits = myGitFile.getCommits()
    print "Commits in log file:  ", len(myCommits)
    for myCommit in myCommits:
        print "\r\nCommit Number:", myCommit.commitNbr, "Added lines:", myCommit.addedLinesInCommit, \
            ".  Deleted lines:", myCommit.deletedLinesInCommit, ".  Test files:", myCommit.testFiles, ".  Production files:", myCommit.prodFiles
        myTrans = myCommit.getTransformations()
        for myTran in myTrans:
            print "Transformations:  ", myTransNames.myName(myTran)
    print "\r\nFiles in logfile:  ", len(myFiles), "\r\n"
    for myFile in myFiles:
        print "\r\n", myFile.fileName, "added in commit:", myFile.commitAdded, ".  Is a test file:",myFile.testFile
        for myCommitDetails in myFile.commitDetails:
            print "\r\nCommit ", myCommitDetails.commitNbr, "Added lines:", myCommitDetails.addedLines, "Deleted lines:", myCommitDetails.deletedLines
            for myMethodName in myCommitDetails.methodNames:
                print "Methods added/modified:", myMethodName
