"""
Created on Nov 20, 2018

@author: susan hammond
Used by:  Assignment
Counts the number of test cases in a test file.
Parameters:

Results:  object containing number of test cases

"""

import sys
import os
import unittest
from unittest.runner import TextTestRunner
import ConfigParser


class GitFile(object):

    def __init__(self):
        nbr_test_cases = 0
        self.myConfig = ConfigParser.ConfigParser()
        self.myConfig.read("TDDanalysis.cfg")
        self.myDrive = self.myConfig.get("Location", "Root")
        self.myHome = self.myConfig.get("Location", "Home")
        self.mySemester = self.myConfig.get("Location", "Semester")
        self.myAssignment = self.myConfig.get("Location", "Assignment")
        self.myProdPath = self.myConfig.get("Location", "ProdPath")
        self.myTestPath = self.myDrive + os.sep + self.myHome + os.sep + self.mySemester + os.sep + self.myAssignment + \
                          os.sep + "submissions"

        self.namePathDepth = self.myConfig.getint("Location", "Name Path Depth")

        nbr_tests_per_class = {}
        test_suite = unittest.TestLoader().discover(ta_path, '*.py')

        for test in test_suite:                                     # Counts number of tests in acceptance test files
            if unittest.suite._isnotsuite(test):
              nbr_tests_per_class[test._test.shortDescription()] = 1
            else:
                for t in test:
                    str_of_testsuite = str(t)
                    testsuite_parts = str_of_testsuite.split("<")
                    if len(testsuite_parts) > 2:
                        class_names = testsuite_parts[2].split(".")
                        class_name = class_names[0].lower()
                        nbr_tests_per_class[class_name] = len(testsuite_parts) - 2
                    else:
                        class_names = testsuite_parts[0].split("(")
                        class_name = class_names[0].lower()
                        nbr_tests_per_class[class_name] = "ModuleImportFailure"
