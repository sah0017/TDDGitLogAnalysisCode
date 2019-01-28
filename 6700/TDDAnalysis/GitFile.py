"""
Created on Jul 10, 2014

@author: susan hammond
Used by:  AnalyzeGitLogFileAndCreateRpt
At a class level, contains Files and File Types found in the git log for this student
Parameters:  Opens git log file and Keeps track of commit data per assignment.

Results:  controls reading through a git file and tracks data about it.
Uses:  Assignment, Commit

"""

# import subprocess
import Assignment
import jsonpickle
import TATestCase
import FileHandler
import os


class GitFile(object):
    """ Analyzes a single git log file """
    Assignment.Assignment.loadAssignments()
    myTATestCase = TATestCase.TATestCase()
    TATestCaseDict = myTATestCase.retrieveTATestCaseObject()
    myFiles = {}                  # a dictionary of pyFile names and their prod/test designation in this git file

    @classmethod
    def getFiles(cls, myAssignment):
        return cls.myFiles

    @classmethod
    def addNewPyFile(cls, new_pyfile):
        cls.myFiles.update({new_pyfile.get_file_name(): new_pyfile.get_file_type()})

    @classmethod
    def newPyFile(cls, py_file_name):
        if cls.myFiles.has_key(py_file_name):
            return False
        else:
            return True

    @classmethod
    def getFileType(cls, py_file_name):
        return cls.myFiles.get(py_file_name)    # the value for this key is prod or test

    def __init__(self):
        """
        Constructor
        """
        self.myAssignmentFileName = ""
        self.myAssignmentsList = []         # a list of all the Assignment instances in this file

    def analyzeGitLogFile(self, file_name):
        """
        :param file_name: The git file it's analyzing

        Controls the looping through the git file"""
        print file_name
        self.myAssignmentFileName = file_name

        my_file_i_o = FileHandler.FileHandler()
        my_file_i_o.open_file(file_name)
        __nextAssignmentName = Assignment.Assignment.originalAssignment     # first assignment name

        my_file_i_o.readNextLine()                                     # first line says commit
        my_file_i_o.readNextLine()                                     # second line has commit date
        while __nextAssignmentName is not False:
            __myAssignment = Assignment.Assignment(__nextAssignmentName)
            __nextAssignmentName = __myAssignment.analyzeAssignment(my_file_i_o)   # reads thru file until it hits a new assignment
            self.myAssignmentsList.append(__myAssignment)

        my_file_i_o.close_file()

    def generate_individual_report(self, path, file_name, which_assignment):

        # list containing all the assignments, which contains a list of all the commits in that assignment
        my_assignments = self.getAssignments()
        out_file = open(path + os.sep + file_name + ".gitout", "w")
        grade_file = open(path + os.sep + file_name + ".txt", "w")
        out_file.write("Assignments in log file:  " + str(len(my_assignments)))
        for myAssignment in my_assignments:
            if which_assignment == "all" or which_assignment.lower() == myAssignment.assignmentName.lower():
                my_commit_stats = myAssignment.CalculateMyCommitStats(out_file, grade_file)
                myAssignment.addCommitTotalsToAssignment(my_commit_stats)
                # myFiles = self.getFiles(myAssignment)
        out_file.close()
        grade_file.close()

    def getAssignments(self):
        return self.myAssignmentsList

    def setAssignments(self, assignment_list):
        self.myAssignmentsList = assignment_list

    def storeGitReportObject(self, file_name):
        out_s = open(file_name + '.json', 'w')

        # Write to the stream
        my_json_string = jsonpickle.encode(self)
        out_s.write(my_json_string)
        out_s.close()
            
    def retrieveGitReportObject(self, filename):
        
        in_s = open(filename+'.json', 'r')
        
        # Read from the stream
        my_json_string = in_s.read()
        try:
            git_report_object = jsonpickle.decode(my_json_string)
        except Exception as e:
            git_report_object = None
        
        in_s.close()
        
        return git_report_object
