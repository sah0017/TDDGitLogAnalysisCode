"""
Created on Jul 1, 2016

@author: susan hammond

This program is called from the AutoGrader batch (for Windows) or shell script (for Mac).  AutoGrader
loops through the list of submissions (created by GetDirectoryList) and passes in the student path and
correct assignment to analyze.
The runTaTests method loads the TA test files and runs the student's tests against the
TA Test code.
"""
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

        ta_results = TATestResults.TATestResults()
        ta_results.total_tests_run = report.testsRun
        ta_results.total_tests_failed = len(report.failures)
        ta_results.total_tests_with_error = len(report.errors)

        failure_stats = self.retrieveTAReportObject(TAAutoGrader.FAIL)
        if failure_stats is None:
            failure_stats = {}
        error_stats = self.retrieveTAReportObject(TAAutoGrader.ERROR)
        if error_stats is None:
            error_stats = {}

        for failed_test_case, failure in report.failures:
            test_case_parts = failed_test_case.id().split(".")
            class_name = test_case_parts[0].lower()
            test_name = test_case_parts[2]
            if class_name in failure_stats:       # Class name for test cases
                if test_name in failure_stats[class_name]:   # test name inside the class
                    failure_stats[class_name][test_name] += 1
                else:
                    failure_stats[class_name] = {}
                    failure_stats[class_name][test_name] = 1
            else:
                failure_stats[class_name] = {}
                failure_stats[class_name][test_name] = 1
            if class_name in ta_results.total_fails_by_testclass:       # Class name for test cases
                ta_results.total_fails_by_testclass[class_name] += 1
            else:
                ta_results.total_fails_by_testclass[class_name] = 1
        for error_case, error in report.errors:
            test_case_parts = error_case.id().split(".")
            class_name = test_case_parts[1].lower()
            test_name = test_case_parts[2]
            if class_name in error_stats:
                if test_name in error_stats[class_name]:   # test name inside the class
                    error_stats[class_name][test_name] += 1
                else:
                    error_stats[class_name] = {}
                    error_stats[class_name][test_name] = 1
            else:
                error_stats[class_name] = {}
                error_stats[class_name][test_name] = 1
            if class_name in ta_results.total_fails_by_testclass:       # Class name for test cases
                ta_results.total_fails_by_testclass[class_name] += 1
            else:
                ta_results.total_fails_by_testclass[class_name] = 1

        self.storeTAReportObject(TAAutoGrader.FAIL, failure_stats)
        self.storeTAReportObject(TAAutoGrader.ERROR, error_stats)

        return ta_results

    def run_ta_tests(self, ta_path, prod_path, assignment):
        sys.path.insert(0, prod_path)

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

        with open(os.path.join(ta_path + assignment + ".TAreport"), "a+") as ta_reportout_file:
            try:
                # os.system("python " + prod_path + os.sep +"microservice.py")
                ta_reportout_file.write("\n\rStudent submission path:  " + prod_path + "\n\r")
                try:
                    with open(os.path.join(ta_path + assignment + ".stream"), "a+") as ta_stream_file:
                        ta_stream_file.write("/n******************************************************************************************\n")
                        ta_stream_file.write("***  Student submission path:  " + prod_path + "\n")
                        ta_stream_file.write("******************************************************************************************\n")
                        ta_report = TextTestRunner(stream=ta_stream_file, verbosity=2).run(test_suite)
                except Exception as e:
                    ta_reportout_file.write("Exception thrown:  " + str(e))
                ta_reportout_file.write("Number of tests run:  " + str(ta_report.testsRun) + "\n\r")
                if ta_report.wasSuccessful():
                    ta_reportout_file.write("All tests completed successfully!  Success rate 100%\n\r")
                else:
                    ta_stats = self.collect_report_stats(ta_report)

                    pass_ratio = ta_stats.passing_test_ratio() * 100
                    ta_reportout_file.write("See log for Content of TestRunner failures.  "
                                            "\nTotal Failures:  " + str(ta_stats.total_tests_failed) +
                                            "\tErrors:  " + str(ta_stats.total_tests_with_error) +
                                            "\tSuccess rate " + format(pass_ratio, ".2f") + "%\r\n")
                    for err_class, count in ta_stats.total_fails_by_testclass.items():
                        if err_class.lower() in nbr_tests_per_class:
                            total_tests_for_class = nbr_tests_per_class[err_class.lower()]
                            pass_ratio = ((total_tests_for_class - count) / float(total_tests_for_class)) * 100
                            ta_reportout_file.write("\nAll Test Failures for " + err_class +
                                                "  :  " + str(count) +
                                                "\tSuccess rate " + format(pass_ratio, ".2f") + "%\r")

            except Exception as e:
                ta_reportout_file.write("Import Error:  " + prod_path + "\n\r" +
                                        "Exception Message:  " + str(e))

            ta_reportout_file.write("\n********************************************************************************\n\r")

    def storeTAReportObject(self, file_name, stats):
        out_s = open(os.path.join(self.TATestPath + os.sep + file_name + '.json'), 'w')

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
            json_string_object = in_s.read()
            t_a_report_object = json.loads(json_string_object)

            '''
            try:
                t_a_report_object = json.load(json_string_object)
            except Exception as e:
                t_a_report_object = None
            '''
            in_s.close()
        except:
            t_a_report_object = None

        return t_a_report_object

    def runAutoGrader(self, total_args):
        if total_args > 1:
            data_file = str(sys.argv[1])
            assignment_str = str(sys.argv[2]).split(".")
            myAutoGrader.assignment = assignment_str[0]
            if self.mySemester == "6700Spring17":
                data_file = data_file + os.sep + "softwareprocess"
        else:
            # data_file = "g:\\git\\6700Spring16\\CA03\\submissions\\yanyufei_late_3331231_73091650_yzy0050CA03\\SoftwareProcess\\SoftwareProcess\\Assignment\\"
            data_file = self.myDrive + os.sep + self.myHome + os.sep + self.mySemester + os.sep + \
                        self.myAssignment + os.sep + "submissions" + os.sep + "pittman-tyler" + os.sep + "softwareprocess"
            myAutoGrader.assignment = self.myAssignment

        myAutoGrader.run_ta_tests(os.path.join(self.TATestPath),
                                  os.path.join(data_file), myAutoGrader.assignment)


if __name__ == '__main__':
    totalArgs = len(sys.argv)
    args = str(sys.argv)

    # print os.getcwd()

    myAutoGrader = TAAutoGrader()
    myAutoGrader.runAutoGrader(totalArgs)
