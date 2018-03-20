'''
Created on May 24, 2016

@author: susanha

TATestCase reads in the TA Test Cases and creates a JSON file that contains the names
of all the test cases, plus the number of lines of code in each test method.
Run this every time new TA Test Cases are added for an assignment.
'''
# from py._iniconfig import SectionWrapper
import ConfigParser
import os
import fnmatch
import jsonpickle

class TATestCase(object):
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        myConfig = ConfigParser.ConfigParser() 
        myConfig.read("TDDanalysis.cfg")
        myDrive = myConfig.get("Location","Root")
        myHome = myConfig.get("Location","Home")
        mySemester = myConfig.get("Location","Semester")
        myTestLocation = myConfig.get("TA Test Case Location","Test Directory")
        self.analysisRoot = os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + myTestLocation)
    
    
    def Walk(self, root='.', recurse=True, pattern='*'):
        """
            Generator for walking a directory tree.
            Starts at specified root folder, returning files
            that match our pattern. Optionally will also
            recurse through sub-folders.
        """
        for path, subdirs, files in os.walk(root):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path, name)
            if not recurse:
                break
    
    def createTATestCaseDict(self, recurse=True):
        """
   
            Sums createTATestCaseDict per method in Python files in the specified folder.
            By default recurses through subfolders.
        """
        if os.path.exists(self.analysisRoot):
            locInMethod = 0
            TATestCaseDict = {}
            for fspec in self.Walk(self.analysisRoot, recurse, '*.py'):
                skip = False
                firstMethodInFile = True
                methodName = ""
                for line in open(fspec).readlines():
                    
                    line = line.strip()
                    if line:
                        if line.startswith('#'):
                            continue
                        if line.startswith('"""'):
                            skip = not skip
                            continue
                        if not skip:
                            if line.startswith("def"):
                                if not firstMethodInFile:
                                    if (methodName != "setUp") and (methodName != "tearDown"):
                                        TATestCaseDict[methodName] = locInMethod
                                    locInMethod = 0
                                firstMethodInFile = False
                                methodData = line.split(" ")
                                methodName = methodData[1].split("(")[0]
    
                            locInMethod += 1
                if (methodName != "setUp") and (methodName != "tearDown"):
                    TATestCaseDict[methodName] = locInMethod
        
            self.storeTATestCaseObject(TATestCaseDict)
    
    def storeTATestCaseObject(self, TATestCaseDict):
        out_s = open(self.analysisRoot+os.sep+'TATestCase.json', 'w')

        # Write to the stream
        myJsonString = jsonpickle.encode(TATestCaseDict)
        out_s.write(myJsonString)
        out_s.close()
            
    def retrieveTATestCaseObject(self):
        
        try:
            with open(self.analysisRoot+os.sep+'TATestCase.json', 'r') as in_s:

                # Read from the stream
                myJsonString = in_s.read()
                TATestCaseDict = jsonpickle.decode(myJsonString)
        except Exception as e:
            TATestCaseDict = None
        

        return TATestCaseDict
      
    
if __name__ == '__main__':
    
    myTestCases = TATestCase()
    myTestCases.createTATestCaseDict()
    TATestCaseDict = myTestCases.retrieveTATestCaseObject()
    for testcase in TATestCaseDict:
        print testcase, TATestCaseDict[testcase]
