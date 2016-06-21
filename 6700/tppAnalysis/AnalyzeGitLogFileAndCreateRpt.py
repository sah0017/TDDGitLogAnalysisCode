'''
Created on Jul 25, 2014

@author: susanha
'''
import GitFile
import os
import Transformations
import AssignmentTotals


class SubmissionReport:

    __totalSubmissions = 0
    __totalCommitsInAnalysis = 0
    __totalTransformationsInAnalysis = 0
    __totalAntiTransformationsInAnalysis = 0
    __totalLinesOfCodeInAnalysis = 0
    
    __transTotalsInAnalysis = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    __antitransTotalsInAnalysis = [0,0,0,0,0,0,0,0,0,0,0,0]
    

        
    def __init__(self):
        pass
        
        
    
    def analyzeGitLog(self, path, fileName):
        self.add_to_total_submissions_in_analysis(1)
        myGitFile = GitFile.GitFile()                       # instantiates a git log file object

        myGitFile.analyzeGitLogFile(path+"\\"+fileName)        # reads through entire git log file and performs TDD/TPP analyzes
        fileParts = os.path.splitext((fileName))
        myAssignments = self.GenerateInvididualReport(path, fileParts[0], myGitFile)
                
        myGitFile.setAssignments(myAssignments)    # Add commit stats to git file object
        myGitFile.storeGitReportObject(path+"\\"+fileParts[0])
    
    

    def GenerateInvididualReport(self, path, fileName, myGitFile):
        myFiles = myGitFile.getFiles()                      # list containing PyFile objects with file name and relevant data
        myAssignments = myGitFile.getAssignments()          # list containing all the assignments, which contains a list of all the commits in that assignment
        outFile = open(path + "\\" + fileName + ".gitout", "w")
        outFile.write("Assignments in log file:  " + str(len(myAssignments)))
        nbrOfAssignments = len(myAssignments)
        for myAssignment in myAssignments:
            myCommitStats = self.CalculateMyCommitStats(outFile, myAssignment)
            myAssignment.addCommitTotalsToAssignment(myCommitStats)
        outFile.write("\r\nFiles in logfile:  " + str(len(myFiles)) + "\r\n")
        for myFile in myFiles:
            outFile.write("\r\n" + myFile.fileName + " added in commit:" + str(myFile.nbrOfCommits) + ".  Is a prod file:" + str(myFile.prodFile))
            for myCommitDetails in myFile.commitDetails:
                outFile.write("\r\n\tAssignment " + str(myCommitDetails.assignmentName) + "\tCommit " + str(myCommitDetails.commitNbr) + ".  Added lines:" + str(myCommitDetails.addedLines) + ".  Deleted lines:" + str(myCommitDetails.deletedLines) + ".  Added TA Test Lines:" + str(myCommitDetails.taTestLines))
                outFile.write("\r\n\t\tMethods added/modified:")
                for myMethod in myCommitDetails.methodNames:
        # for myMethodName in myMethod.methodName:
                    outFile.write("\r\t\t" + myMethod.methodName)
        
        outFile.close()
        return myAssignments

    def CalculateMyCommitStats(self, outFile, myAssignment):
        myTransNames = Transformations.Trans()
        transTotalsInAssignment = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        antitransTotalsInAssignment = [0,0,0,0,0,0,0,0,0,0,0,0]
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
        outFile.write("\r\nAssignment Name:" + str(myAssignment.assignmentName))
        nbrCommits = nbrCommits + len(myAssignment.myCommits)
        for myCommit in myAssignment.myCommits:
            outFile.write("\r\n\tCommit Number:" + str(myCommit.commitNbr) + "\tCommit type: " + myCommit.commitType + "\tAdded lines:" + str(myCommit.addedLinesInCommit) + ".  Deleted lines:" + str(myCommit.deletedLinesInCommit) + ".\r\n\t  Added test lines:" + str(myCommit.addedTestLOC) + "  Deleted test lines:" + str(myCommit.deletedTestLOC) + ".\r\n\t  Test files:" + str(myCommit.nbrTestFiles) + ".  Production files:" + str(myCommit.nbrProdFiles) + ".  Number of Transformations:  " + str(myCommit.numberOfTransformations) + ". \n\r")
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
            outFile.write("\tTransformations:")
            for myTran in myTrans:
                outFile.write("\r\t" + myTransNames.getTransformationName(myTran))
                if myTran >= 0:
                    self.__transTotalsInAnalysis[myTran] = self.__transTotalsInAnalysis[myTran] + 1
                    transTotalsInAssignment[myTran] = transTotalsInAssignment[myTran] + 1
                    nbrTransformations = nbrTransformations + 1
                else:
                    self.__antitransTotalsInAnalysis[abs(myTran)] = self.__antitransTotalsInAnalysis[abs(myTran)] + 1
                    antitransTotalsInAssignment[abs(myTran)] = antitransTotalsInAssignment[abs(myTran)] + 1
                    nbrAntiTransformations = nbrAntiTransformations + 1
        
        overallDeletedLines = deletedLines + deletedTestLines
        outFile.write("\r\nTotal test code lines added:" + str(addedTestLines))
        outFile.write("\r\nTotal production code lines added:" + str(addedLines))
        outFile.write("\r\nTotal test code lines deleted:" + str(deletedTestLines))
        outFile.write("\r\nTotal production code lines deleted:" + str(deletedLines))
        if addedLines > 0:
            ratio = addedTestLines / float(addedLines)
            outFile.write("\r\nRatio of test code to production code:" + format(ratio, '.2f') + ":1")
        self.add_to_total_commits_in_analysis(nbrCommits)
        self.__totalTransformationsInAnalysis = self.__totalTransformationsInAnalysis + nbrTransformations
        self.__totalAntiTransformationsInAnalysis = self.__totalAntiTransformationsInAnalysis + nbrAntiTransformations
        self.__totalLinesOfCodeInAnalysis = self.__totalLinesOfCodeInAnalysis + addedLines
        myCommitStats = AssignmentTotals.AssignmentTotals()
        myCommitStats.nbrCommits = nbrCommits
        myCommitStats.RLCommit = nbrRedLight
        myCommitStats.GLCommit = nbrGreenLight
        myCommitStats.refCommit = nbrRefactor
        myCommitStats.otherCommit = nbrUnknownCommit
        myCommitStats.addedLinesInAssignment = addedLines
        myCommitStats.addedTestLOCInAssignment = addedTestLines
        myCommitStats.deletedLinesInAssignment = deletedLines
        myCommitStats.deletedTestLOCInAssignment = deletedTestLines
        myCommitStats.totalDelLines = overallDeletedLines
        myCommitStats.totalTransByTypeInAssignment = transTotalsInAssignment
        myCommitStats.totalAntiTransByTypeInAssignment = antitransTotalsInAssignment
        return myCommitStats

    @classmethod
    
    def get_total_commits(cls):
        return cls.__totalCommitsInAnalysis

    @classmethod

    def get_total_transformations(cls):
        return cls.__totalTransformationsInAnalysis

    @classmethod

    def get_total_anti_transformations(cls):
        return cls.__totalAntiTransformationsInAnalysis

    @classmethod

    def get_total_lines_of_code(cls):
        return cls.__totalLinesOfCodeInAnalysis

    @classmethod
    def get_total_submissions(cls):
        return cls.__totalSubmissions

    @classmethod

    def get_trans_totals_by_tran_type(cls):
        return cls.__transTotalsInAnalysis

    @classmethod

    def get_antitrans_totals_by_tran_type(cls):
        return cls.__antitransTotalsInAnalysis

    @classmethod

    def set_total_commits(cls, value):
        cls.__totalCommitsInAnalysis = value
    @classmethod

    def add_to_total_commits_in_analysis(cls, value):
        cls.__totalCommitsInAnalysis = cls.__totalCommitsInAnalysis + value
    @classmethod
        
    def set_total_transformations(cls, value):
        cls.__totalTransformationsInAnalysis = value

    @classmethod

    def set_total_anti_transformations(cls, value):
        cls.__totalAntiTransformationsInAnalysis = value

    @classmethod
    
    def set_total_lines_of_code(cls, value):
        cls.__totalLinesOfCodeInAnalysis = value

    @classmethod
    def set_total_submissions(cls, value):
        cls.__totalSubmissions = value
    @classmethod
        
    def add_to_total_submissions_in_analysis(cls, value):
        cls.__totalSubmissions = cls.__totalSubmissions + value
    @classmethod


    def set_trans_totals_by_tran_type(cls, value):
        cls.__transTotalsInAnalysis = value

    @classmethod

    def set_antitrans_totals_by_tran_type(cls, value):
        cls.__antitransTotalsInAnalysis = value

    @classmethod

    def del_total_commits(cls):
        del cls.__totalCommitsInAnalysis
    @classmethod


    def del_total_transformations(cls):
        del cls.__totalTransformationsInAnalysis

    @classmethod

    def del_total_anti_transformations(cls):
        del cls.__totalAntiTransformationsInAnalysis

    @classmethod

    def del_total_lines_of_code(cls):
        del cls.__totalLinesOfCodeInAnalysis

    @classmethod
    def del_total_submissions(cls):
        del cls.__totalSubmissions

    @classmethod

    def del_trans_totals(cls):
        del cls.__transTotalsInAnalysis

    @classmethod

    def del_antitrans_totals(cls):
        del cls.__antitransTotalsInAnalysis
    '''    
    __totalCommitsInAnalysis = property(get_total_commits, set_total_commits, del_total_commits, "totalCommits's docstring")
    __totalTransformationsInAnalysis = property(get_total_transformations, set_total_transformations, del_total_transformations, "totalTransformations's docstring")
    __totalAntiTransformationsInAnalysis = property(get_total_anti_transformations, set_total_anti_transformations, del_total_anti_transformations, "totalAntiTransformations's docstring")
    __totalLinesOfCodeInAnalysis = property(get_total_lines_of_code, set_total_lines_of_code, del_total_lines_of_code, "totalLinesOfCode's docstring")
    #__totalSubmissions = property(get_total_submissions, set_total_submissions, del_total_submissions, "totalSubmissions's docstring")
    __transTotalsInAnalysis = property(get_trans_totals_by_tran_type, set_trans_totals_by_tran_type, del_trans_totals, "transTotals's docstring")
    __antitransTotalsInAnalysis = property(get_antitrans_totals_by_tran_type, set_antitrans_totals_by_tran_type, del_antitrans_totals, "antitransTotals's docstring")
    '''
