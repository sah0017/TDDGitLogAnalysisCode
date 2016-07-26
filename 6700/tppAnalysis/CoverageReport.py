'''
Created on Apr 25, 2016

@author: susanha

'''

from CodeCoverage import CodeCoverage 
import os
import re
import time



class CodeCoverageAnalysisReport():
    
    def __init__(self):
        self.path = "g:\\git\\6700Spring16\\CA02\\"
        self.exclude = "*.pyc"
        self.ignore = ""
        self.no_assert = True
        self.multi = False
        

    def createCoverageAnalysisReport(self):
        
        myAssignment = "CA02"
        includePath = ""
        myCoverageAnalysis = CodeCoverage()
        reportLocation = os.path.join(self.path)
        with open(reportLocation + myAssignment + ".cvgrpt", "w") as outFile :
            outFile.write("Module Name\t\tCode Coverage percentage\n\r")
        with open(reportLocation + myAssignment + ".result", "w") as resultoutFile:
            resultoutFile.write("Run date/time:  " + time.strftime("%a, %d %b %Y %H:%M:%S")+"\n\r")
        for root, myDir, files in os.walk(self.path + "\\submissions"):
            if re.search("test", root):
                if not re.search("__MACOSX",root):
                    nameSplit = root.split("\\")
                    if nameSplit[len(nameSplit)-1] == "__pycache__":
                        nameSplit = nameSplit[:len(nameSplit)-1]
                    print nameSplit
                    for i in range(0,len(nameSplit)-1):
                        includePath = includePath + nameSplit[i] + "\\"
                    print includePath
                    myCoverageAnalysis = CodeCoverage()
                    myCCPct = myCoverageAnalysis.analyzeCodeCoverage(includePath, myAssignment)
                    time.sleep(2)
                    fileName = nameSplit[6]
                    studentName = fileName.split("_")
                    with open(reportLocation + "\\" +myAssignment + ".cvgrpt", "a+") as outFile:
                        outFile.write("\n\r" + studentName[0] + "\t\t" + format(myCCPct, ".2f"))
                    includePath = ""
        

if __name__ == '__main__':
    
    myCCReport = CodeCoverageAnalysisReport()
    myCCReport.createCoverageAnalysisReport()
