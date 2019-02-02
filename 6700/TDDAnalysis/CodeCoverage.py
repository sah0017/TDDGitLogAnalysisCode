"""
Created on Jul 1, 2016

@author: susanha

This program is called from the CodeCovAnalysis batch (for Windows) or shell script (for Mac).  CodeCovAnalysis
loops through the list of submissions and passes in the student path and assignment.
analyzeCodeCoverage method loops through the student's submission, finds and loads test files, starts
the code coverage analyzer, runs the student's tests against the student's code, then stops the CC analyzer.
"""
import sys, subprocess, signal
import os
import re
import unittest
import coverage
from unittest.runner import TextTestRunner
from coverage.misc import CoverageException
import time
import traceback
from contextlib import contextmanager
# from py._iniconfig import SectionWrapper
import ConfigParser

errorDict = {-1: "Coverage Exception",
             -2: "Run Error",
             -3: "Import Error/Didn't get to student's tests"}
SUBPATH = 0
PRODPATH = 1
TESTPATH = 2
FILENAME = 3
SANDBOX = 4


@contextmanager
def redirect_stdout(new_target):
    old_target, sys.stdout = sys.stdout, new_target
    try:
        yield new_target
    finally:
        sys.stdout = old_target


class CodeCoverage(object):
    def __init__(self):
        """
        Constructor
        """
         
        # myConfig = ConfigParser.ConfigParser()
        # myConfig.read("analysis.cfg")
        # self.root = myConfig.get("Location","Root")
        self.assignment = ""
        self.dataFile = ""
        self.namePathDepth = 0
        self.CCReport = {}

    def retrieve_code_coverage_for_specific_student_and_assignment(self, student_name, assignment_name):
        """ Not currently used. """

        cc_pct = "N/A"
        a_lc = assignment_name.lower()
        try:
            students = self.CCReport[a_lc].split()
            try:
                index = students.index(student_name)
                cc_pct = students[index+1]
                print cc_pct
            except:
                cc_pct = "CC Error"    # student not found
        except:
            pass    # assignment not in code coverage list
        return cc_pct

    def loadCoverageReports(self, root, assignment_list):
        """ Not currently used. """
        for assignment in assignment_list:
            a_lc = assignment.lower()
            cc_file_name = root + os.sep + assignment + os.sep + assignment + ".cvgrpt"
            try:
                cc_file = open(cc_file_name, "r")
                self.CCReport[a_lc] = cc_file.read()
                cc_file.close()
            except Exception as e:
                pass    # report not found

        return

    def findStudentTestFiles(self, root, prod):
        paths = ["", "", "", "", ""]
        paths[SUBPATH] = ""
        name_split = root.split(os.sep)
        file_name = name_split[self.namePathDepth]
        paths[SUBPATH] = os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep)
        student_name = file_name.split("_")
        print student_name[0]
        prod_path = os.path.join(root + os.sep + prod)
        if os.path.exists(os.path.join(prod_path, "prod")):  # there is a prod directory under prod dir
            prod_path = os.path.join(prod_path + os.sep + "prod")
        if os.path.exists(os.path.join(root, "test")):  # test directory is under root dir
            test_path = os.path.join(root + os.sep + "test")
        else:                                            # test directory is under prod directory
            test_path = os.path.join(prod_path + os.sep + "test")
        if os.path.exists(os.path.join(root, "sandbox")):  # sandbox directory is under root dir
            sandbox_path = os.path.join(root + os.sep + "sandbox")
        else:                                            # sandbox directory is under prod directory
            sandbox_path = os.path.join(prod_path + os.sep + "sandbox")
        paths[SUBPATH] = paths[SUBPATH]
        paths[PRODPATH] = prod_path
        paths[TESTPATH] = test_path
        paths[FILENAME] = file_name
        paths[SANDBOX] = sandbox_path
        if os.path.exists(test_path):      # test directory is off of the student ID directory
            test_files = os.listdir(test_path)
        else:
            test_path = os.path.join(root + os.sep + prod + os.sep + "test")  # test directory is under softwareprocess dir
            test_files = os.listdir(test_path)
        return test_files, paths, student_name[0]

    def analyzeCodeCoverage(self, root, prod_path, assignment, html_report):
        test_env = {}
        print root
        test_files, paths, stu_name = self.findStudentTestFiles(root, prod_path)
        if not os.path.exists(os.path.join(paths[SUBPATH] + os.sep + "coverage")):
            os.mkdir(os.path.join(paths[SUBPATH] + os.sep + "coverage"))
        try:
            test_env['COVERAGE_PROCESS_START'] = ".coveragerc"
            #test_env['FLASK_ENV'] = "TEST"
            #test_env['FLASK_APP'] = "microservice.py"

            cov = coverage.Coverage(source=[paths[PRODPATH], root],
                                    omit=[paths[TESTPATH] + os.sep + '*', paths[SANDBOX] + os.sep + '*', '__init__.py'],
                                    branch=True, cover_pylib=False)
            # cov = coverage.Coverage(source=[root])
            with open(os.path.join(paths[SUBPATH] + assignment + ".TestRunReport"), "a+") as cc_report_outfile:
                cc_report_outfile.write("\n\rStudent submission and path:  " + root + "\n\r")
            prod_files = os.listdir(paths[PRODPATH])
            sys.path.insert(0, root)
            sys.path.insert(0, paths[PRODPATH])
            sys.path.insert(0, paths[TESTPATH])
            os.chdir(root)

            #test_process = subprocess.Popen(["coverage run --source microservice.main"], env=test_env, shell=True)
            #test_process.communicate(add_url_rule('/shutdown', 'shutdown', shutdown,
            #                         methods=['POST', 'GET']))

            os.chdir(paths[PRODPATH])
            my_test_loader = unittest.TestLoader()
            test = re.compile(r"\b.py\b", re.IGNORECASE)      # test is a compiled regular expression to search for python files
            test_files = filter(test.search, test_files)        # this will filter out any files that aren't python files
            prod_files = filter(test.search, prod_files)
            filename_to_module_name = lambda f: os.path.splitext(f)[0]  # this removes the python extension from test files
            module_test_names = map(filename_to_module_name, test_files)
            # moduleProdNames = map(filename_to_module_name, prod_files)

            cov.start()


            with open(os.path.join(paths[SUBPATH] + assignment + ".TestRunReport"), "a+") as cc_report_outfile:
                cc_report_outfile.write("Test File Names\n\r")

            for t in test_files:
                with open(os.path.join(paths[SUBPATH] + assignment + ".TestRunReport"), "a+") as cc_report_outfile:
                    cc_report_outfile.write(t + "\r")

            load = my_test_loader.loadTestsFromNames(module_test_names)

            cc_report = TextTestRunner().run(load)

            with open(os.path.join(paths[SUBPATH] + assignment + ".TestRunReport"), "a+") as cc_report_outfile:
                cc_report_outfile.write("Number of tests run:  " + str(cc_report.testsRun) + "\n\r")

                if not cc_report.wasSuccessful():

                    cc_report_outfile.write("Content of TestRunner failures\r")

                    for failedTestCase, failure in cc_report.failures:
                        cc_report_outfile.write(str(failedTestCase) + failure + "\n\r")

                else:

                    cc_report_outfile.write("All tests completed successfully!\n\r")

                cc_report_outfile.write("********************************************************************************")
            #test_process.terminate()  # Send the signal to all the process groups

            cov.stop()
            cov.save()
            cov.combine()


        except Exception as e:
            with open(os.path.join(paths[SUBPATH] + assignment + ".TestRunReport"), "a+") as cc_report_outfile:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback, file=cc_report_outfile)
            # return -3, studentName[0]



        # if CCreport.wasSuccessful():
        try:
            # print root
            if html_report:
                my_html_drive = myConfig.get("Location", "Root")
                my_html_home = myConfig.get("Location", "Home")
                my_html_semester = myConfig.get("Location", "Semester")
                my_html_assignment = myConfig.get("Location", "Assignment")
                html_path = os.path.join(my_html_drive + os.sep + my_html_home + os.sep + my_html_semester + os.sep + my_html_assignment + os.sep + stu_name)
                if not (os.path.exists(html_path)):
                    os.mkdir(html_path)
                pctg = cov.html_report(directory=html_path)
            with open(os.path.join(paths[SUBPATH] + assignment + ".TestRunReport"), "a+"):

                outfile = open(os.path.join(paths[SUBPATH] + os.sep + "coverage" + os.sep + paths[FILENAME] + assignment + ".cvg"), "a+")
                pctg = cov.report(file=outfile)
                outfile.close()

            pctg = cov.report(omit=[paths[TESTPATH] + os.sep + '*', paths[SANDBOX] + os.sep + '*', '__init__.py'])
            # print pctg
            # raw_input("Continue (success)?")

            return pctg, stu_name
        except CoverageException as ce:
            print "CoverageException testpath:  " + paths[TESTPATH] + "\t" + str(ce)
            with open(os.path.join(paths[SUBPATH] + assignment + ".TestRunReport"), "a+") as cc_report_outfile:
                cc_report_outfile.write("CoverageException " + str(ce) + "\n\r")
                cc_report_outfile.write("********************************************************************************")
            # raw_input("Continue (CoverageException)?")
            return -1, stu_name

        finally:
            print "Test cases not successful at " + paths[TESTPATH]
            with open(os.path.join(paths[SUBPATH] + assignment + ".TestRunReport"), "a+") as cc_report_outfile:
                cc_report_outfile.write("\nTest cases not successful \n\r")
                cc_report_outfile.write("********************************************************************************")

            # raw_input("Continue (CCreport not successful)?")
            return -2, stu_name


if __name__ == '__main__':
    totalArgs = len(sys.argv)
    args = str(sys.argv)

    # print os.getcwd()
    myConfig = ConfigParser.ConfigParser()
    myConfig.read("TDDanalysis.cfg")
    myDrive = myConfig.get("Location", "Root")
    myHome = myConfig.get("Location", "Home")
    mySemester = myConfig.get("Location", "Semester")
    myProdPath = myConfig.get("Location", "ProdPath")
    myAssignment = myConfig.get("Location", "Assignment")
    TATestLocation = myConfig.get("TA Test Case Location", "Test Directory")

    myCodeCoverage = CodeCoverage()
    myCodeCoverage.namePathDepth = myConfig.getint("Location", "Name Path Depth")

    with open(os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + myAssignment +
              os.sep + myCodeCoverage.assignment + ".cvgrpt"), "a+") as outFile:
        outFile.write("Module Name\t\tCode Coverage percentage\n\r")
    with open(os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + myCodeCoverage.assignment+".TestRunReport"), "a+") as cc_report_outfile:
        cc_report_outfile.write("Run date/time:  " + time.strftime("%a, %d %b %Y %H:%M:%S") + "\n\r")

    if totalArgs > 1:
        dataFile = str(sys.argv[1])
        assignmentStr = str(sys.argv[2]).split(".")
        myCodeCoverage.assignment = assignmentStr[0]
        if str(sys.argv[3]) == "yes":
            htmlReport = True
        else:
            htmlReport = False 
    else:
        # dataFile = "g:\\git\\6700Spring16\\CA03\\submissions\\yanyufei_late_3331231_73091650_yzy0050CA03\\SoftwareProcess\\SoftwareProcess\\Assignment\\"
        dataFile = myDrive + os.sep + myHome + os.sep + mySemester + os.sep + myAssignment + os.sep + "submissions" + os.sep + "chlundy"
        myCodeCoverage.assignment = myAssignment
        htmlReport = False

    myPct, sName = myCodeCoverage.analyzeCodeCoverage(dataFile, myProdPath, myCodeCoverage.assignment, htmlReport)
    print myPct, sName
    with open(os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + myAssignment+os.sep+myCodeCoverage.assignment+".cvgrpt"), "a+") as outFile:
        if myPct < 0:
            outFile.write("\n\r" + sName + "\t\t" + errorDict[myPct])
        else:
            outFile.write("\n\r" + sName + "\t\t" + format(myPct, ".2f"))
