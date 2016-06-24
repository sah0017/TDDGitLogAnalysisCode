'''
Created on Apr 25, 2016

@author: susanha

'''

import CodeCoverage
import os
import re
import json
import pkgutil
import pkgutil

class RadonArguments():
    
    def __init__(self):
        self.path = "g:\\git\\6700Spring16\\CA05"
        self.exclude = "*.pyc"
        self.ignore = ""
        self.no_assert = True
        self.multi = False
        
def GetTestNames(path):
  """Returns a list of the names of the test modules in gslib.tests."""
  matcher = re.compile(r'^def test')
  names = []
  for _, modname, _ in pkgutil.iter_modules(path):
    m = matcher.match(modname)
    if m:
      names.append(m.group('name'))
  return names    

def createCoverageAnalysisReport():
    configArgs = RadonArguments()
    
    myDrive = "g:\\"
#printToFile = raw_input("Print output to file?  ")
    mySemester = "6700Spring16"
    myDirectory = "CA05"
    includePath = ""
    reportLocation = os.path.join(myDrive,"git",mySemester)
    #outFile = open(myDrive + "git\\" + mySemester + "\\" + myDirectory + "radon.rept", "a")
    #outFile.write("CC Rank\tModule Name\t\tMaintainability Index\tMI Rank\n")
    for root, myDir, files in os.walk(myDrive + "git\\" + mySemester + "\\" + myDirectory + "\\submissions"):
        if re.search("test", root):
            names = GetTestNames(root)
            for name in names:
                print name
            nameSplit = root.split("\\")
            for i in range(0,len(nameSplit)-2):
                includePath = includePath + nameSplit[i] + "\\"
            myCoverageAnalysis = CodeCoverage.CodeCoverage(myDrive, mySemester)
            for myFile in files:
                if (myFile.endswith(".py") and (not myFile.startswith("._")) and (myFile != '__init__.py')):
                    #os.chdir(myDir)
                    print root + "\\" + myFile
                    dataFile = os.path.join(root,nameSplit[5],myFile)
                    testFile = os.path.join(root, myFile)
                    myCoverageAnalysis.analyzeCodeCoverage(dataFile,testFile,includePath)
                    '''
                    if results != None:
                        for module, ma in results:
                            outFile.write(ma + "\t\t" + module + "\t")
                    '''
            includePath = ""
    #outFile.close()

if __name__ == '__main__':
    
    createCoverageAnalysisReport()
