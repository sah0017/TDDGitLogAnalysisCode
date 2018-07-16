'''
Created on July 16, 2018

@author: susanha

TATestResults is a class to hold a summary of the results from all students for all the TA test cases run.
'''


class TATestResults(object):

    def __init__(self):
        self.student_id = ""
        self.total_tests_run = 0
        self.total_tests_with_error = 0
        self.total_tests_failed = 0


    def passing_test_ratio(self):
        ratio = (self.total_tests_run - self.total_tests_with_error - self.total_tests_failed) / float(self.total_tests_run)
        return ratio
