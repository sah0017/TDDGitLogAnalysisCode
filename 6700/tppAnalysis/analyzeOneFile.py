'''
Created on Sep 17, 2014

@author: susanha
'''
import os
import subprocess
import AssignmentTotals
import AnalyzeGitLogFileAndCreateRpt
import FormattedGitLog
import Assignment
import CreateGitfileAnalysisReport


if __name__ == '__main__':
    #  antley--matthew_1247150_45465189_mra0016Log
    #  romanowski--brenden_481945_45480789_btr0005Log
    #  bryant--james_2270195_45451066_jab0091Log
    root = "g:\\"
    myDrive = "g:\\"
    mySemester = "6700Spring16\\"
    myDirectory = "CA02\\"
    currentDir = "git\\6700Spring16\\CA02\\submissions\\stelljessica_3072097_71347590_jrs0067ca02\\SoftwareProcess"                
    fileName = "stelljessica_3072097_71347590_jrs0067ca02"                

    myFormattedGitLog = FormattedGitLog.FormattedGitLog()
    myFormattedGitLog.formatGitLogOutput(root, currentDir, myDrive, mySemester, myDirectory,fileName)

    myAssignment = AnalyzeGitLogFileAndCreateRpt.SubmissionReport()
    myAnalysis = AnalyzeGitLogFileAndCreateRpt.SubmissionReport()
    myAnalysis.analyzeGitLog(myDrive + "git\\" + mySemester + "\\" + myDirectory, fileName+"log.gitdata")
    
    '''
         
    myReport = CreateGitfileAnalysisReport.AnalysisReport()
    myReport.createAnalysisReport(myDrive, "yes",mySemester,"mha0012")
    myCommitStatsList = myAssignment.get_my_commit_totals()
    for myCommitStats in myCommitStatsList:
        print fileName, myCommitStats.get_nbr_commits(), myCommitStats.get_rlcommit(), myCommitStats.GLCommit, myCommitStats.refCommit, myCommitStats.otherCommit, myCommitStats.avgLinesPerCommit, myCommitStats.avgTransPerCommit, myCommitStats.ratioTestToProd, myCommitStats.totalDelLines
    '''