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
        self.path = "g:\\git\\6700Spring16\\CA05"
        self.exclude = "*.pyc"
        self.ignore = ""
        self.no_assert = True
        self.multi = False
    
def createComplexityAnalysisReport():
    configArgs = RadonAnalysis()
    
    
    myDrive = "g:\\"
#printToFile = raw_input("Print output to file?  ")
    mySemester = "6700Spring16"
    myAssignment = "CA05"
    outFile = open(myDrive + "git\\" + mySemester + "\\" + myAssignment + "radon.rept", "a")
    outFile.write("CC Rank\tModule Name\t\tMaintainability Index\tMI Rank\n")
    for root, myDir, files in os.walk(myDrive + "git\\" + mySemester + "\\" + myAssignment + "\\submissions"):
        nameSplit = root.split("\\")
        myComplexityAnalysis = CodeComplexity.CodeComplexity(myDrive, mySemester)
        if (re.search("prod", root) or re.search("test", root)):
            for myFile in files:
                if (myFile.endswith(".py") and (not myFile.startswith("._")) and (myFile != '__init__.py')):
                    #os.chdir(myDir)
                    print root + "\\" + myFile
                    configArgs.path = os.path.join(root, myFile)
                    results, mi_results = myComplexityAnalysis.analyzeComplexity(configArgs)
                    if results != None:
                        for module, ma in results:
                            mar = cc_rank(ma)
                            outFile.write(mar + "\t\t" + module + "\t")
                   
                    if mi_results != None and len(mi_results) > 0:
                        for mi, rank in mi_results:
                            outFile.write(format(mi, ".2f") + "\t" + rank+ "\n")
                    
    outFile.close()

if __name__ == '__main__':
    
    createComplexityAnalysisReport()
