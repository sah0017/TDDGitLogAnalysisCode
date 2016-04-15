'''
Created on Sep 17, 2014

@author: susanha
'''
import os
import subprocess
import AssignmentCommitTotals
import AnalyzeAGitLogFileAndCreateGitoutFile

if __name__ == '__main__':
    #  antley--matthew_1247150_45465189_mra0016Log
    #  romanowski--brenden_481945_45480789_btr0005Log
    #  bryant--james_2270195_45451066_jab0091Log
    path = "g:\\git\\6700Spring16\\CA02\\submissionsLate\\seayedward_648520_71341383_ers0007CA02\\SoftwareProcess"                
    fileName = "seayedward_648520_71341383_ers0007CA02Log"                

    os.chdir(path+"\\.git")
    p=subprocess.Popen(["git","whatchanged","-p","-m","--reverse","--pretty=format:\"commit %h%n%ad%n%s\""],stdout=subprocess.PIPE)
    outFile = open(path + "\\" + fileName, "w")
    for line in p.stdout.readlines():
        outFile.write(line)
    outFile.close()

    myResults = AnalyzeAGitLogFileAndCreateGitoutFile.Results()
    myCommitStats = myResults.analyzeGitLog(path + "\\", fileName)
    print fileName, myCommitStats.nbrCommits, myCommitStats.RLCommit, myCommitStats.GLCommit, myCommitStats.refCommit, myCommitStats.otherCommit, myCommitStats.avgLinesPerCommit, myCommitStats.avgTransPerCommit, myCommitStats.ratioTestToProd, myCommitStats.totalDelLines
