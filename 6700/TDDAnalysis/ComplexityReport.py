'''
Created on Apr 25, 2016

@author: susanha

'''

import CodeComplexity
import os
import re
import json
from radon.cli import Config
from radon.complexity import cc_rank
from types import NoneType

class RadonAnalysis():
    
    def __init__(self):
        self.path = "/Users/shammond/Google Drive/6700Spring17"
        self.exclude = "*.pyc"
        self.ignore = ""
        self.no_assert = True
        self.multi = False
    
def createComplexityAnalysisReport():
    configArgs = RadonAnalysis()
    
    
    myDrive = "/Users/shammond/Google Drive"
    mySemester = "6700Spring17"
    myAssignment = "Assignment5"
    outFile = open(myDrive + os.sep + mySemester + os.sep + myAssignment + "radon.csv", "a+")
    outFile.write("CC Rank, Module Name, Maintainability Index,MI Rank\n")
    for root, myDir, files in os.walk(myDrive + os.sep + mySemester + os.sep + myAssignment + os.sep + "submissions"):
        nameSplit = root.split(os.sep)
        myComplexityAnalysis = CodeComplexity.CodeComplexity(myDrive, mySemester)
        if (re.search("prod", root) or re.search("test", root) or re.search("softwareprocess", root)):
            for myFile in files:
                if (myFile.endswith(".py") and (not myFile.startswith("._")) and (myFile != '__init__.py')):
                    #os.chdir(myDir)
                    print root + os.sep + myFile
                    configArgs.path = os.path.join(root, myFile)
                    results, mi_results = myComplexityAnalysis.analyzeComplexity(configArgs)
                    if results is not None and len(results) > 0:
                        for module, ma in results:
                            mar = cc_rank(ma)
                            outFile.write(mar + "," + nameSplit[7] + os.sep + myFile + ",")
                    else:
                        outFile.write("Missing, " + nameSplit[7] + os.sep + myFile + ",")
                   
                    if mi_results is not None and len(mi_results) > 0:
                        for mi, rank in mi_results:
                            outFile.write(format(mi, ".2f") + ", " + rank + "\n")
                    else:
                        outFile.write("Missing, Missing\n")
    outFile.close()

if __name__ == '__main__':
    
    createComplexityAnalysisReport()
