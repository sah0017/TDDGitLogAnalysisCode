'''
Created on Sep 17, 2014

@author: susanha
Stub file to perform the analysis on one specific file
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
    root = "/Users"
    myDrive = "shammond/GoogleDrive"
    mySemester = "6700Spring18"
    myAssignment = "spring2018-rcube"
    currentDir = "shammond/GoogleDrive/6700Spring18/spring2018-rcube/submissions/spring2018-rcube-aht0006/"
    fileName = "aht0006"
    analysisRoot = os.path.join(root, myDrive, mySemester, myAssignment)

    myFormattedGitLog = FormattedGitLog.FormattedGitLog()
    myFormattedGitLog.formatGitLogOutput(root, currentDir, analysisRoot,fileName)

    #myAssignment = AnalyzeGitLogFileAndCreateRpt.SubmissionReport()
    myAnalysis = AnalyzeGitLogFileAndCreateRpt.SubmissionReport()
    filename_extension = fileName + ".gitdata"
    myAnalysis.analyzeGitLog(os.path.join(root, myDrive, mySemester, myAssignment), filename_extension, "all")
    
    '''
         
    myReport = CreateGitfileAnalysisReport.AnalysisReport()
    myReport.createAnalysisReport(myDrive, "yes",mySemester,"mha0012")
    myCommitStatsList = myAssignment.get_my_commit_totals()
    for myCommitStats in myCommitStatsList:
        print fileName, myCommitStats.get_nbr_commits(), myCommitStats.get_rlcommit(), myCommitStats.GLCommit, myCommitStats.refCommit, myCommitStats.otherCommit, myCommitStats.avgLinesPerCommit, myCommitStats.avgTransPerCommit, myCommitStats.ratioTestToProd, myCommitStats.totalDelLines
    '''
