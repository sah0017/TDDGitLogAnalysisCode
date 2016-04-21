'''
Created on Sep 17, 2014

@author: susanha
'''
import os
import subprocess
import AssignmentCommitTotals
import AnalyzeAGitLogFileAndCreateIndivRpt
import FormattedGitLog
import Assignment


if __name__ == '__main__':
    #  antley--matthew_1247150_45465189_mra0016Log
    #  romanowski--brenden_481945_45480789_btr0005Log
    #  bryant--james_2270195_45451066_jab0091Log
    root = "g:\\"
    myDrive = "g:\\"
    myDirectory = "6700Spring16\\"
    mySemester = "CA02\\"
    currentDir = "git\\6700Spring16\\CA02\\submissionsLate\\seayedward_648520_71341383_ers0007CA02\\SoftwareProcess"                
    fileName = "seayedward_648520_71341383_ers0007CA02Log"                

    myFormattedGitLog = FormattedGitLog.FormattedGitLog()
    myFormattedGitLog.formatGitLogOutput(root, currentDir, myDrive, mySemester, myDirectory,fileName)

    myAssignment = AnalyzeAGitLogFileAndCreateIndivRpt.IndividualReport()
    
    '''
    myCommitStatsList = myAssignment.get_my_commit_totals()
    for myCommitStats in myCommitStatsList:
        print fileName, myCommitStats.get_nbr_commits(), myCommitStats.get_rlcommit(), myCommitStats.GLCommit, myCommitStats.refCommit, myCommitStats.otherCommit, myCommitStats.avgLinesPerCommit, myCommitStats.avgTransPerCommit, myCommitStats.ratioTestToProd, myCommitStats.totalDelLines
    '''