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
    myGitFile = GitFile.GitFile("c:\\Users\\susanha\\git\\6700test\\revLogfile")
    myGitFile.readGitFile()
    myFiles = myGitFile.getFiles()
    myCommits = myGitFile.getCommits()
    print "Commits in log file:  ", len(myCommits)
    for myCommit in myCommits:
        print "Commit Number:  ", myCommit.commitNbr, "Added lines in commit", myCommit.addedLinesInCommit, \
            ".  Deleted lines in commit", myCommit.deletedLinesInCommit, "Test files:  ", myCommit.testFiles, "Production files:  ", myCommit.prodFiles
        myTrans = myCommit.getTransformations()
        for myTran in myTrans:
            print "Transformations:  ", myTran
    print "Files in logfile:  ", len(myFiles)
    for myFile in myFiles:
        print myFile.fileName, "Added in commit:  ", myFile.commitAdded, myFile.testFile
