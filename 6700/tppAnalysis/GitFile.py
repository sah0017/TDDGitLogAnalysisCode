'''
Created on Jul 10, 2014

@author: susanha
'''

# import subprocess
import Assignment
import jsonpickle
import TATestCase
import FileHandler
import os




class GitFile(object):
    " Analyzes a single git log file"


    Assignment.Assignment.loadAssignments()
    myTATestCase = TATestCase.TATestCase()
    TATestCaseDict = myTATestCase.retrieveTATestCaseObject()
    myFiles = {}                  # a dictionary of pyFile names and their prod/test designation in this git file


    @classmethod
    def getFiles(cls, myAssignment):
        return cls.myFiles

    @classmethod
    def addNewPyFile(cls, newPyFile):
        cls.myFiles.update({newPyFile.getFileName(): newPyFile.getFileType()})

    @classmethod
    def newPyFile(cls, pyFileName):
        if cls.myFiles.has_key(pyFileName):
            return False
        else:
            return True

    @classmethod
    def getFileType(cls, pyFileName):
        return cls.myFiles.get(pyFileName)    # the value for this key is prod or test


    def __init__(self):
        '''
        Constructor
        '''
        self.myAssignmentFileName = ""
        self.myAssignmentsList = []         # a list of all the Assignment instances in this file

    def analyzeGitLogFile(self, fileName):
        "Controls the looping through the git file"
        print fileName
        self.myAssignmentFileName = fileName

        myFileIO = FileHandler.FileHandler()
        myFileIO.open_file(fileName)
        __nextAssignmentName = Assignment.Assignment.originalAssignment     # first assignment name

        myFileIO.readNextLine()                                     # first line says commit
        myFileIO.readNextLine()                                     # second line has commit date
        while __nextAssignmentName != False:
            __myAssignment = Assignment.Assignment(__nextAssignmentName)
            __nextAssignmentName = __myAssignment.analyzeAssignment(myFileIO)   # reads thru file until it hits a new assignment
            self.myAssignmentsList.append(__myAssignment)

        myFileIO.close_file()

    def GenerateInvididualReport(self, path, fileName):
        # list containing PyFile objects with file name and relevant data
        # myFiles = []
        # list containing all the assignments, which contains a list of all the commits in that assignment
        myAssignments = self.getAssignments()
        outFile = open(path + os.sep + fileName + ".gitout", "w")
        outFile.write("Assignments in log file:  " + str(len(myAssignments)))
        for myAssignment in myAssignments:
            myCommitStats = myAssignment.CalculateMyCommitStats(outFile)
            myAssignment.addCommitTotalsToAssignment(myCommitStats)
            # myFiles = self.getFiles(myAssignment)
        '''     not storing data like this any more
        outFile.write("\r\n**********************************************\r\nFiles in logfile:  " +
                      str(len(myFiles)) + "\r\n")
        for myFile in myFiles:
            outFile.write("\r\n----------------------------------------------\r\n" + myFile.fileName +
                          " added in commit:" + str(myFile.nbrOfCommits) + ".  Is a prod file:" + str(myFile.isProdFile()))
            for myCommitDetails in myFile.commitDetails:
                outFile.write("\r\n\tAssignment " + str(myCommitDetails.assignmentName) + "\tCommit " +
                              str(myCommitDetails.commitNbr) + ".  Added lines:" + str(myCommitDetails.addedLines) +
                              ".  Deleted lines:" + str(myCommitDetails.deletedLines) + ".  Added TA Test Lines:" +
                              str(myCommitDetails.taTestLines))
                outFile.write("\r\n\t\tMethods added/modified:")
                for myMethod in myCommitDetails.methodNames:
        # for myMethodName in myMethod.methodName:
                    outFile.write("\r\t\t" + myMethod.methodName)
        '''
        outFile.close()

    def getAssignments(self):
        return self.myAssignmentsList

    def setAssignments(self,assignmentList):
        self.myAssignmentsList = assignmentList

    def storeGitReportObject(self, fileName):
        out_s = open(fileName+'.json', 'w')

        # Write to the stream
        myJsonString = jsonpickle.encode(self)
        out_s.write(myJsonString)
        out_s.close()
            
    def retrieveGitReportObject(self,filename):
        
        in_s = open(filename+'.json', 'r')
        
        # Read from the stream
        myJsonString = in_s.read()
        try:
            gitReportObject = jsonpickle.decode(myJsonString)
        except Exception as e:
            gitReportObject = None
        
        in_s.close()
        
        return gitReportObject
