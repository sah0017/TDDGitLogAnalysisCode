'''
Created on Jul 1, 2016

@author: susanha

This program is called from the AutoGrader batch (for Windows) or shell script (for Mac).  AutoGrader
loops through the list of submissions (created by GetDirectoryList) and passes in the student path and
correct assignment to analyze.
The runTaTests method loads the TA test files and runs the student's tests against the
TA Test code.
'''
import sys, os, re, unittest, coverage
from unittest.runner import TextTestRunner
import ConfigParser
import json
import TATestResults


class TAAutoGrader(object):
    FAIL = "fail_report"
    ERROR = "error_report"

    def __init__(self):
        self.myConfig = ConfigParser.ConfigParser()
        self.myConfig.read("TDDanalysis.cfg")
        self.myDrive = self.myConfig.get("Location","Root")
        self.myHome = self.myConfig.get("Location","Home")
        self.mySemester = self.myConfig.get("Location","Semester")
        self.myAssignment = self.myConfig.get("Location","Assignment")
        self.myProdPath = self.myConfig.get("Location","ProdPath")
        self.TATestLocation = self.myConfig.get("TA Test Case Location", "Test Directory")
        self.TATestPath = self.myDrive + os.sep + self.myHome + os.sep + self.mySemester + os.sep + self.TATestLocation
        self.namePathDepth = self.myConfig.getint("Location","Name Path Depth")

    def collect_report_stats(self, report):

        failure_stats = self.retrieveTAReportObject(TAAutoGrader.FAIL)
        if failure_stats is None:
            failure_stats = {}
        error_stats = self.retrieveTAReportObject(TAAutoGrader.ERROR)
        if error_stats is None:
            error_stats = {}

        for failed_test_case, failure in report.failures:
            if failure_stats.has_key(failed_test_case._testMethodName):
                failure_stats[failed_test_case._testMethodName] += 1
            else:
                failure_stats[failed_test_case._testMethodName] = 1
        for error_case, error in report.errors:
            if error_stats.has_key(error_case._testMethodName):
                error_stats[error_case._testMethodName] += 1
            else:
                error_stats[error_case._testMethodName] = 1

        self.storeTAReportObject(TAAutoGrader.FAIL, failure_stats)
        self.storeTAReportObject(TAAutoGrader.ERROR, error_stats)

    def run_ta_tests(self, ta_path, prod_path, assignment):
        sys.stdout = open(ta_path + os.sep + 'ta_test.stdout.log', 'a+')

        sys.path.insert(0, prod_path)

        test_suite = unittest.TestLoader().discover(ta_path, '*.py')

        with open(os.path.join(ta_path + assignment + ".TAreport"), "a+") as ta_reportout_file:
            try:
                sys.stdout.write("/n******************************************************************************************\n")
                sys.stdout.write("***  Student submission path:  " + prod_path + "\n")
                sys.stdout.write("******************************************************************************************\n")
                #os.system("python " + prod_path + os.sep +"microservice.py")
                ta_reportout_file.write("\n\rStudent submission path:  " + prod_path + "\n\r")
                try:
                    with open(os.path.join(ta_path + assignment + ".stream"), "a+") as ta_stream_file:
                        ta_report = TextTestRunner(stream=ta_stream_file, verbosity=2).run(test_suite)
                except Exception as e:
                    ta_reportout_file.write("Exception thrown:  " + str(e))
                ta_reportout_file.write("Number of tests run:  " + str(ta_report.testsRun) + "\n\r")
                if ta_report.wasSuccessful():
                    ta_reportout_file.write("All tests completed successfully!  Success rate 100%\n\r")
                else:
                    self.collect_report_stats(ta_report)
                    ta_stats = TATestResults.TATestResults()

                    ta_stats.total_tests_run = ta_report.testsRun
                    ta_stats.total_tests_failed = len(ta_report.failures)
                    ta_stats.total_tests_with_error = len(ta_report.errors)
                    pass_ratio = ta_stats.passing_test_ratio() * 100
                    ta_reportout_file.write("See log for Content of TestRunner failures.  "
                                            "Failures:  " + str(ta_stats.total_tests_failed) +
                                            "\nErrors:  " + str(ta_stats.total_tests_with_error) +
                                            "\nSuccess rate " + format(pass_ratio, ".2f") + "%\r")
            except Exception as e:
                ta_reportout_file.write("Import Error:  " + prod_path + "\n\r" +
                                        "Exception Message:  " + str(e))

            ta_reportout_file.write("\n********************************************************************************\n\r")

    def storeTAReportObject(self, fileName, stats):
        out_s = open(os.path.join(self.TATestPath + os.sep + fileName + '.json'), 'w')

        # Write to the stream
        try:
            json.dump(stats, out_s, sort_keys=True)
        except Exception as e:
            print e
        out_s.close()

    def retrieveTAReportObject(self,filename):
        try:
            in_s = open(os.path.join(self.TATestPath + os.sep + filename +'.json'), 'r')

            # Read from the stream
            JSonStringObject = in_s.read()
            TAReportObject = json.loads(JSonStringObject)

            '''
            try:
                TAReportObject = json.load(JSonStringObject)
            except Exception as e:
                TAReportObject = None
            '''
            in_s.close()
        except:
            TAReportObject = None

        return TAReportObject

    def runAutoGrader(self, totalArgs):
        if totalArgs > 1:
            data_file = str(sys.argv[1])
            assignment_str = str(sys.argv[2]).split(".")
            myAutoGrader.assignment = assignment_str[0]
        else:
            #data_file = "g:\\git\\6700Spring16\\CA03\\submissions\\yanyufei_late_3331231_73091650_yzy0050CA03\\SoftwareProcess\\SoftwareProcess\\Assignment\\"
            data_file = self.myDrive + os.sep + self.myHome + os.sep + self.mySemester + os.sep + \
                        self.myAssignment + os.sep + "submissions" + os.sep + "spring2018-rcube-aza0092"
            myAutoGrader.assignment = self.myAssignment

        myAutoGrader.run_ta_tests(os.path.join(self.TATestPath),
                                  os.path.join(data_file), myAutoGrader.assignment)

if __name__ == '__main__':
    totalArgs = len(sys.argv)
    args = str(sys.argv)

    #print os.getcwd()

    myAutoGrader = TAAutoGrader()
    myAutoGrader.runAutoGrader(totalArgs)

