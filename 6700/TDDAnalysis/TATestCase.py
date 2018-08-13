"""
Created on May 24, 2016

@author: susan hammond

TATestCase reads in the TA Test Cases and creates a JSON file that contains the names
of all the test cases, plus the number of lines of code in each test method.
Run this every time new TA Test Cases are added for an assignment.
"""
# from py._iniconfig import SectionWrapper
import ConfigParser
import os
import fnmatch
import jsonpickle


class TATestCase(object):
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """
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
            loc_in_method = 0
            t_a_test_case_dict = {}
            for fspec in self.Walk(self.analysisRoot, recurse, '*.py'):
                skip = False
                first_method_in_file = True
                method_name = ""
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
                                if not first_method_in_file:
                                    if (method_name != "setUp") and (method_name != "tearDown"):
                                        t_a_test_case_dict[method_name] = loc_in_method
                                    loc_in_method = 0
                                first_method_in_file = False
                                method_data = line.split(" ")
                                method_name = method_data[1].split("(")[0]
    
                            loc_in_method += 1
                if (method_name != "setUp") and (method_name != "tearDown"):
                    t_a_test_case_dict[method_name] = loc_in_method
        
            self.storeTATestCaseObject(t_a_test_case_dict)
    
    def storeTATestCaseObject(self, t_a_test_case_dict):
        out_s = open(self.analysisRoot+os.sep+'TATestCase.json', 'w')

        # Write to the stream
        my_json_string = jsonpickle.encode(t_a_test_case_dict)
        out_s.write(my_json_string)
        out_s.close()
            
    def retrieveTATestCaseObject(self):
        
        try:
            with open(self.analysisRoot+os.sep+'TATestCase.json', 'r') as in_s:

                # Read from the stream
                my_json_string = in_s.read()
                t_a_test_case_dict = jsonpickle.decode(my_json_string)
        except Exception as e:
            t_a_test_case_dict = None

        return t_a_test_case_dict
      
    
if __name__ == '__main__':
    
    myTestCases = TATestCase()
    myTestCases.createTATestCaseDict()
    TATestCaseDict = myTestCases.retrieveTATestCaseObject()
    for testcase in TATestCaseDict:
        print testcase, TATestCaseDict[testcase]
