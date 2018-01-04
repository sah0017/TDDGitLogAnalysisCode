'''
Created on Apr 25, 2016

@author: susanha

'''

from CodeCoverage import CodeCoverage 
import os
import re
import time
import ConfigParser



class CodeCoverageAnalysisReport():
    
    def __init__(self):
        myConfig = ConfigParser.ConfigParser() 
        myConfig.read("TDDanalysis.cfg")
        myDrive = myConfig.get("Location","Root")
        myHome = myConfig.get("Location","Home")
        printToFile = True
        mySemester = myConfig.get("Location","Semester")
        self.myAssignment = myConfig.get("Location","Assignment")
        myTestLocation = myConfig.get("TA Test Case Location","Test Directory")
        analysisRoot = os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + self.myAssignment)
        reportRoot = os.path.join(myDrive + os.sep + myHome + os.sep + mySemester)
        namePathDepth = myConfig.getint("Location","Name Path Depth")
    
        self.path = analysisRoot    # old, hard-coded location "g:\\git\\6700Spring16\\CA02\\"
        self.exclude = "*.pyc"
        self.ignore = ""
        self.no_assert = True
        self.multi = False
        

    def createCoverageAnalysisReport(self):
        
        includePath = ""
        myCoverageAnalysis = CodeCoverage()
        self.path = self.path
        with open(self.path + self.myAssignment + ".cvgrpt", "w") as outFile :
            outFile.write("Module Name\t\tCode Coverage percentage\n\r")
        with open(self.path + self.myAssignment + ".result", "w") as resultoutFile:
            resultoutFile.write("Run date/time:  " + time.strftime("%a, %d %b %Y %H:%M:%S")+"\n\r")
        for root, myDir, files in os.walk(self.path + os.sep + "submissions"):
            if re.search("test", root):
                if not re.search("__MACOSX",root):
                    nameSplit = root.split(os.sep)
                    if nameSplit[len(nameSplit)-1] == "__pycache__":
                        nameSplit = nameSplit[:len(nameSplit)-1]
                    print nameSplit
                    for i in range(0,len(nameSplit)-1):
                        includePath = includePath + nameSplit[i] + os.sep
                    print includePath
                    myCoverageAnalysis = CodeCoverage()
                    myCCPct = myCoverageAnalysis.analyzeCodeCoverage(includePath, self.myAssignment)
                    time.sleep(2)
                    fileName = nameSplit[6]
                    studentName = fileName.split("_")
                    with open(self.path + os.sep +self.myAssignment + ".cvgrpt", "a+") as outFile:
                        outFile.write("\n\r" + studentName[0] + "\t\t" + format(myCCPct, ".2f"))
                    includePath = ""
        

if __name__ == '__main__':
    
    myCCReport = CodeCoverageAnalysisReport()
    myCCReport.createCoverageAnalysisReport()
