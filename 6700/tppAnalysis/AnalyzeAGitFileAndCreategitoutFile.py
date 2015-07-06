'''
Created on Jul 25, 2014

@author: susanha
'''
import GitFile
import Transformations
import Commit
import codecs

class Results:
    
    def __init__(self,assignment):
        self.totalCommits = 0
        self.totalTransformations = 0
        self.totalAntiTransformations = 0
        self.totalLinesOfCode = 0
        self.totalSubmissions = 0
        self.assignment = assignment
        self.transTotals = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.antitransTotals = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        
    
    def printResults(self, path, fileName):
        myTransNames = Transformations.Trans()
        myGitFile = GitFile.GitFile(path+"\\"+fileName,self.assignment)
        self.totalSubmissions = self.totalSubmissions + 1
        myGitFile.readGitFile()
        myFiles = myGitFile.getFiles()
        myCommits = myGitFile.getCommits()
        addedLines = 0
        addedTestLines = 0
        deletedLines = 0
        deletedTestLines = 0
        
        nbrTransformations = 0
        nbrAntiTransformations = 0
        ratio = 0
        outFile = open(path+"\\"+fileName+".gitout", "w")
        outFile.write( "Commits in log file:  " + str(len(myCommits)))
        nbrOfCommits = len(myCommits)
        self.totalCommits = self.totalCommits + nbrOfCommits
        for myCommit in myCommits:
            outFile.write("\r\nCommit Number:"+ str(myCommit.commitNbr) + "  Added lines:" + str(myCommit.addedLinesInCommit) +
                ".  Deleted lines:" + str(myCommit.deletedLinesInCommit) + ".\r\n  Added test lines:"+ str(myCommit.addedTestLOC)+
                "  Deleted test lines:" + str(myCommit.deletedTestLOC) + ".\r\n  Test files:" + str(myCommit.testFiles) + 
                ".  Production files:" + str(myCommit.prodFiles) + ".  Number of Transformations:  "+ str(myCommit.numberOfTransformations)+". \n\r")
            addedLines = addedLines + myCommit.addedLinesInCommit
            addedTestLines = addedTestLines + myCommit.addedTestLOC
            deletedLines = deletedLines + myCommit.deletedLinesInCommit
            deletedTestLines = deletedTestLines + myCommit.deletedTestLOC
            
            myTrans = myCommit.getTransformations()
            outFile.write("Transformations:")
            for myTran in myTrans:
                outFile.write("\r" + myTransNames.myName(myTran))
                if myTran >= 0:
                    self.transTotals[myTran] = self.transTotals[myTran]+1
                    nbrTransformations = nbrTransformations + 1
                else:
                    self.antitransTotals[abs(myTran)] = self.antitransTotals[abs(myTran)]+1
                    nbrAntiTransformations = nbrAntiTransformations + 1
        outFile.write("\r\nTotal test code lines added:"+str(addedTestLines))
        outFile.write("\r\nTotal production code lines added:"+str(addedLines))
        outFile.write("\r\nTotal test code lines deleted:"+str(deletedTestLines))
        outFile.write("\r\nTotal production code lines deleted:"+str(deletedLines))
        if addedLines > 0:
            ratio = addedTestLines/float(addedLines)
            outFile.write("\r\nRatio of test code to production code:" + format(ratio,'.2f')+":"+str(addedLines/addedLines))
        self.totalTransformations = self.totalTransformations + nbrTransformations
        self.totalAntiTransformations = self.totalAntiTransformations + nbrAntiTransformations
        self.totalLinesOfCode = self.totalLinesOfCode + addedLines
        outFile.write("\r\nFiles in logfile:  " + str(len(myFiles)) + "\r\n")
        for myFile in myFiles:
            outFile.write("\r\n" + myFile.fileName + " added in commit:" + str(myFile.commitAdded) + ".  Is a prod file:" + str(myFile.prodFile))
            for myCommitDetails in myFile.commitDetails:
                outFile.write("\r\n\tCommit " + str(myCommitDetails.commitNbr) + ".  Added lines:" + str(myCommitDetails.addedLines) + 
                              ".  Deleted lines:" + str(myCommitDetails.deletedLines))
                outFile.write("\r\n\t\tMethods added/modified:" )
                for myMethod in myCommitDetails.methodNames:
                    # for myMethodName in myMethod.methodName:
                    outFile.write("\r\t\t" + myMethod.methodName)
                
        outFile.close()
        overallDeletedLines = deletedLines + deletedTestLines
        if nbrOfCommits > 0:
            return nbrOfCommits, addedLines/float(nbrOfCommits), nbrTransformations/float(nbrOfCommits), ratio, overallDeletedLines
        else:
            return 0,0,0,ratio, overallDeletedLines
    