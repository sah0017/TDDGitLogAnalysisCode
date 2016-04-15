'''
Created on Jul 25, 2014

@author: susanha
'''
import GitFile
import Transformations
import Commit
import Assignment
import codecs
import AssignmentCommitTotals

class Results:

    
    
    def __init__(self):
        self.totalCommits = 0
        self.totalTransformations = 0
        self.totalAntiTransformations = 0
        self.totalLinesOfCode = 0
        self.totalSubmissions = 0
        #self.assignment = assignment
        self.transTotals = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.antitransTotals = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        
    
    def analyzeGitLog(self, path, fileName):
        myTransNames = Transformations.Trans()
        myGitFile = GitFile.GitFile()
        self.totalSubmissions = self.totalSubmissions + 1
        myGitFile.readGitLogFile(path+"\\"+fileName)
        myFiles = myGitFile.getFiles()
        myAssignments = myGitFile.getAssignments()
        addedLines = 0
        addedTestLines = 0
        deletedLines = 0
        deletedTestLines = 0
        nbrCommits = 0
        nbrRedLight = 0
        nbrGreenLight = 0
        nbrRefactor = 0
        nbrUnknownCommit = 0
        nbrTransformations = 0
        nbrAntiTransformations = 0
        ratio = 0
        outFile = open(path+"\\"+fileName+".gitout", "w")
        outFile.write( "Assignments in log file:  " + str(len(myAssignments)))
        nbrOfAssignments = len(myAssignments)
        for myAssignment in myAssignments:
            outFile.write("\r\nAssignment Number:"+str(myAssignment.assignmentNbr))
            nbrCommits = nbrCommits + len(myAssignment.myCommits)
            for myCommit in myAssignment.myCommits:
                outFile.write("\r\nCommit Number:"+ str(myCommit.commitNbr) + "Commit type: " + myCommit.commitType +  "\tAdded lines:" + str(myCommit.addedLinesInCommit) +
                    ".  Deleted lines:" + str(myCommit.deletedLinesInCommit) + ".\r\n  Added test lines:"+ str(myCommit.addedTestLOC)+
                    "  Deleted test lines:" + str(myCommit.deletedTestLOC) + ".\r\n  Test files:" + str(myCommit.nbrTestFiles) + 
                    ".  Production files:" + str(myCommit.nbrProdFiles) + ".  Number of Transformations:  "+ str(myCommit.numberOfTransformations)+". \n\r")
                if myCommit.commitType.startswith("Red Light"):
                    nbrRedLight = nbrRedLight + 1
                elif myCommit.commitType.startswith("Green Light"):
                    nbrGreenLight = nbrGreenLight + 1
                elif myCommit.commitType.startswith("Refactor"):
                    nbrRefactor = nbrRefactor + 1
                else:
                    nbrUnknownCommit = nbrUnknownCommit + 1
                addedLines = addedLines + myCommit.addedLinesInCommit
                addedTestLines = addedTestLines + myCommit.addedTestLOC
                deletedLines = deletedLines + myCommit.deletedLinesInCommit
                deletedTestLines = deletedTestLines + myCommit.deletedTestLOC
                
                myTrans = myCommit.get_transformations()
                outFile.write("Transformations:")
                for myTran in myTrans:
                    outFile.write("\r" + myTransNames.getTransformationName(myTran))
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
            self.totalCommits = self.totalCommits + nbrCommits
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
        if nbrCommits > 0:
            myCommitStats = AssignmentCommitTotals.AssignmentCommitTotals(nbrCommits, nbrRedLight, nbrGreenLight, nbrRefactor, nbrUnknownCommit, addedLines/float(nbrCommits), nbrTransformations/float(nbrCommits), ratio, overallDeletedLines)
        else:
            myCommitStats = AssignmentCommitTotals.AssignmentCommitTotals(0,0,0,0,0,0,0,ratio, overallDeletedLines)
        return myCommitStats
    
    
    
    def get_total_commits(self):
        return self.__totalCommits


    def get_total_transformations(self):
        return self.__totalTransformations


    def get_total_anti_transformations(self):
        return self.__totalAntiTransformations


    def get_total_lines_of_code(self):
        return self.__totalLinesOfCode


    def get_total_submissions(self):
        return self.__totalSubmissions


    def get_trans_totals(self):
        return self.__transTotals


    def get_antitrans_totals(self):
        return self.__antitransTotals


    def set_total_commits(self, value):
        self.__totalCommits = value


    def set_total_transformations(self, value):
        self.__totalTransformations = value


    def set_total_anti_transformations(self, value):
        self.__totalAntiTransformations = value


    def set_total_lines_of_code(self, value):
        self.__totalLinesOfCode = value


    def set_total_submissions(self, value):
        self.__totalSubmissions = value


    def set_trans_totals(self, value):
        self.__transTotals = value


    def set_antitrans_totals(self, value):
        self.__antitransTotals = value


    def del_total_commits(self):
        del self.__totalCommits


    def del_total_transformations(self):
        del self.__totalTransformations


    def del_total_anti_transformations(self):
        del self.__totalAntiTransformations


    def del_total_lines_of_code(self):
        del self.__totalLinesOfCode


    def del_total_submissions(self):
        del self.__totalSubmissions


    def del_trans_totals(self):
        del self.__transTotals


    def del_antitrans_totals(self):
        del self.__antitransTotals

    totalCommits = property(get_total_commits, set_total_commits, del_total_commits, "totalCommits's docstring")
    totalTransformations = property(get_total_transformations, set_total_transformations, del_total_transformations, "totalTransformations's docstring")
    totalAntiTransformations = property(get_total_anti_transformations, set_total_anti_transformations, del_total_anti_transformations, "totalAntiTransformations's docstring")
    totalLinesOfCode = property(get_total_lines_of_code, set_total_lines_of_code, del_total_lines_of_code, "totalLinesOfCode's docstring")
    totalSubmissions = property(get_total_submissions, set_total_submissions, del_total_submissions, "totalSubmissions's docstring")
    transTotals = property(get_trans_totals, set_trans_totals, del_trans_totals, "transTotals's docstring")
    antitransTotals = property(get_antitrans_totals, set_antitrans_totals, del_antitrans_totals, "antitransTotals's docstring")