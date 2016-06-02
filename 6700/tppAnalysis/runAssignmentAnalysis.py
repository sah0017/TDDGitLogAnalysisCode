'''
Created on Sep 12, 2014

@author: susanha
'''
import os
import AnalyzeGitLogFileAndCreateRpt
import CreateAnalysisReport
import FormattedGitLog


if __name__ == '__main__':
    
    myDrive = "g:\\"
    printToFile = raw_input("Print output to file?  ")
    mySemester = "6700Spring16"
    myDirectory = "CA05"
    myFormattedGitLog = FormattedGitLog.FormattedGitLog()
    ''' 
    for root, myDir, files in os.walk(myDrive + "git\\" + mySemester + "\\" + myDirectory + "\\submissions"):
        nameSplit = root.split("\\")
        for currentDir in myDir:
            if currentDir.endswith(".git"):
                #os.chdir(myDir)
                print nameSplit[4], "Git directory", os.path.join(root, currentDir)
                myFormattedGitLog.formatGitLogOutput(root, currentDir,myDrive, mySemester, myDirectory,nameSplit[5])    
    '''    
    myAnalysis = AnalyzeGitLogFileAndCreateRpt.SubmissionReport()
    for gitDataFile in os.listdir(myDrive + "git\\" + mySemester + "\\" + myDirectory):
        if gitDataFile.endswith(".gitdata"):
            myAnalysis.analyzeGitLog(myDrive + "git\\" + mySemester + "\\" + myDirectory, gitDataFile)
         
    myReport = CreateAnalysisReport.AnalysisReport()
    myReport.createAnalysisReport(myDrive, printToFile,mySemester,myDirectory)