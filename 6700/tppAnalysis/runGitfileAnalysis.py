'''
Created on Sep 12, 2014

@author: susanha

This is the main program that controls all the Git file analysis.
'''
import os
import AnalyzeGitLogFileAndCreateRpt
import CreateGitfileAnalysisReport
import FormattedGitLog

import ConfigParser
from TATestCase import TATestCase


if __name__ == '__main__':
    
    myConfig = ConfigParser.ConfigParser() 
    myConfig.read("TDDanalysis.cfg")
    myDrive = myConfig.get("Location","Root")
    myHome = myConfig.get("Location","Home")
    printToFile = True
    mySemester = myConfig.get("Location","Semester")
    myAssignment = myConfig.get("Location","Assignment")
    myTestLocation = myConfig.get("TA Test Case Location","Test Directory")
    analysisRoot = os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + myAssignment)
    reportRoot = os.path.join(myDrive + os.sep + myHome + os.sep + mySemester)
    namePathDepth = myConfig.getint("Location","Name Path Depth")
    myFormattedGitLog = FormattedGitLog.FormattedGitLog()

    gitfileCreation = raw_input("Have you created the formatted git files? (y/n)  ")

    if gitfileCreation.strip() == "n":                  # This stuff creates the formatted git log output.  Don't need to create this again if we just want to re-run the analysis
        myWorkingDirectory = os.getcwd()   # formatGitLogOutput changes the directory, it needs to be set back before create TATestCaseDict
        for root, myDir, files in os.walk(analysisRoot + os.sep + "submissions"):
            nameSplit = root.split(os.sep)
            for currentDir in myDir:
                if currentDir.endswith(".git"):
                    #os.chdir(myDir)
                    print "Git directory", os.path.join(root, currentDir)
                    myFormattedGitLog.formatGitLogOutput(root, currentDir,analysisRoot,nameSplit[namePathDepth])
        os.chdir(myWorkingDirectory)
        myTATestCase = TATestCase() 
        TATestCaseDict = myTATestCase.createTATestCaseDict()
  
        
    gitfileAnalysis = raw_input("Have you analyzed the formatted git files? (y/n)  ")

    if gitfileAnalysis.strip() == "n":                  # This stuff creates the formatted git log output.  Don't need to create this again if we just want to re-run the analysis
        whichAssignment = raw_input("Report on all assignments or just 1 (type 'all' or assignment Name)  ")
        myAnalysis = AnalyzeGitLogFileAndCreateRpt.SubmissionReport()
        for gitDataFile in os.listdir(analysisRoot):
            if gitDataFile.endswith(".gitdata"):
                myAnalysis.analyzeGitLog(analysisRoot, gitDataFile, whichAssignment)
         
    myReport = CreateGitfileAnalysisReport.AnalysisReport()
    myReport.createAnalysisReport(reportRoot, analysisRoot, printToFile, myAssignment)
