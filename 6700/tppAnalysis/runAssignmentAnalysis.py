'''
Created on Sep 12, 2014

@author: susanha
'''
import os
import AnalyzeAGitLogFileAndCreateIndivRpt
import Transformations
import Assignment
import AssignmentCommitTotals
import CreateAnalysisReport
import FormattedGitLog
import AnalysisRunTotals


if __name__ == '__main__':
    
    myDrive = "g:\\"
    printToFile = raw_input("Print output to file?  ")
    mySemester = "6700Spring16"
    myDirectory = "CA02"
    myFormattedGitLog = FormattedGitLog.FormattedGitLog()
    myAnalysisRunTotals = AnalysisRunTotals.AnalysisRunTotals()
    
    for root, myDir, files in os.walk(myDrive + "git\\" + mySemester + "\\" + myDirectory + "\\submissionsLate"):
                nameSplit = root.split("\\")
                for currentDir in myDir:
                    if currentDir.endswith(".git"):
                        #os.chdir(myDir)
                        print nameSplit[4], "Git directory", os.path.join(root, currentDir)
                        myFormattedGitLog.formatGitLogOutput(root, currentDir,myDrive, mySemester, myDirectory,nameSplit[5])        
    
                        AnalyzeAGitLogFileAndCreateIndivRpt.IndividualReport(myAnalysisRunTotals)
         
    CreateAnalysisReport(myDrive, printToFile,mySemester,myDirectory)