'''
Created on Jul 10, 2014

@author: susanha
'''

# import subprocess
from Transformations import Trans
import codecs
import Commit
import PyFile
import Assignment
import re
import Method
import jsonpickle
from DeletedLine import DeletedLine
from time import strptime
import TATestCase



class GitFile(object):
    " Analyzes a single git log file"

    myTrans = Trans()

    line = ''

    @classmethod
    def readNextLine(self, gitFile):
        try:
            line = gitFile.next()
            return line
        except StopIteration as e:
            return False

    def __init__(self, fileName):
        '''
        Constructor
        '''

        self.myAssignmentsList = []
        self.myFiles = []
        Assignment.Assignment.loadAssignments()
        self.myAssignmentNameDict = Assignment.Assignment.get_assignment_name_dict()
        self.keyIndexList = self.myAssignmentNameDict.keys()
        self.keyIndexList.sort()
        self.originalAssignmentName = Assignment.Assignment.getMyFirstAssignment()
        self.gitFile = codecs.open(fileName)
        print fileName

    def analyzeGitLogFile(self):
        "Controls the looping through the git file"
        __currAssignmentName = self.originalAssignmentName     # first assignment name
        __myAssignment = Assignment.Assignment(__currAssignmentName)
        myTATestCase = TATestCase.TATestCase()
        self.TATestCaseDict = myTATestCase.retrieveTATestCaseObject()

        __commits = 0
        prevCommit = None
        GitFile.readNextLine(self.gitFile)                                     # first line says commit
        for line in self.gitFile:
            __assignmentName = self.findCurrentAssignment(line)  # advances to next line to check the commit date
            if __currAssignmentName != __assignmentName:
                __currAssignmentName = __assignmentName
                self.myAssignmentsList.append(__myAssignment)
                __commits = 0
                __myAssignment = Assignment.Assignment(__currAssignmentName)

            __commitType = self.getCommitType()       # advances to next line to get commit type
            if prevCommit == __commitType:            # looking for consecutive Red or Green Lights
                if __commitType.startswith("Red Light"):
                    __myAssignment.incrementConsecutiveRedLights()
                elif __commitType.startswith("Green Light"):
                    __myAssignment.incrementConsecutiveGreenLights()
            prevCommit = __commitType
            __commits = __commits + 1
            myNewCommit = Commit.Commit(__currAssignmentName, __commitType, __commits)

            __myAssignment.addCommitToAssignment(myNewCommit.analyzeCommit(self.gitFile))

        # save last Assignment in the file to Assignments List
        self.myAssignmentsList.append(__myAssignment)
        self.gitFile.close()

    def getCommitType(self):
        line = self.readNextLine()             # advance to next line to get commit type
        commitType = line.strip()
        self.readNextLine()         # advance to next line to get the first file name in the commit
        return commitType


    def findCurrentAssignment(self, line):
        " a git file can contain multiple assignments.  This is looking for the current one for analysis."
        #self.line = self.readNextLine()         # line after commit contains the commit date
        dateLine = line.split("-")
        commitDate = strptime(dateLine[0].strip(), '%a %b %d %X %Y')
        #commitDay = int(dateLine[2])
        #commitYear = int(dateLine[4])
        #commitDate = date(commitYear,commitMonth,commitDay)

        currAssignmentName = None
        if commitDate <= self.myAssignmentNameDict[self.keyIndexList[0]]:
            currAssignmentName = self.originalAssignmentName
        else:
            for k in range(0, len(self.keyIndexList)-1):
                if (self.myAssignmentNameDict[self.keyIndexList[k]] <= commitDate <= self.myAssignmentNameDict[self.keyIndexList[k+1]]):
                    currAssignmentName = self.keyIndexList[k+1]
        return currAssignmentName

    
    def getAssignments(self):
        return self.myAssignmentsList

    def setAssignments(self,assignmentList):
        self.myAssignmentsList = assignmentList

    def getFiles(self):
        return self.myFiles
    
    def addNewPyFile(self, newPyFile):
        self.myFiles.append(newPyFile)

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
