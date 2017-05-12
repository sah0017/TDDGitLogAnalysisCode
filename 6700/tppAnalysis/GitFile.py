'''
Created on Jul 10, 2014

@author: susanha
'''

# import subprocess
import codecs
import Assignment
import jsonpickle
import TATestCase




class GitFile(object):
    " Analyzes a single git log file"


    line = ''
    Assignment.Assignment.loadAssignments()
    myAssignmentNameDict = Assignment.Assignment.get_assignment_name_dict()
    keyIndexList = myAssignmentNameDict.keys()
    keyIndexList.sort()
    originalAssignmentName = Assignment.Assignment.getMyFirstAssignment()
    myTATestCase = TATestCase.TATestCase()
    TATestCaseDict = myTATestCase.retrieveTATestCaseObject()

    @classmethod
    def is_first_assignment(cls, commitDate):
        if commitDate <= GitFile.myAssignmentNameDict[GitFile.keyIndexList[0]]:
            return True
        else:
            return False

    '''
    This method uses the date on the commit to determine which assignment the commit goes with
    '''
    @classmethod
    def get_curr_assignmentName(cls, commitDate):
        for k in range(0, len(GitFile.keyIndexList)-1):
            if (GitFile.myAssignmentNameDict[GitFile.keyIndexList[k]] <= commitDate <= GitFile.myAssignmentNameDict[GitFile.keyIndexList[k+1]]):
                return GitFile.keyIndexList[k+1]


    @classmethod
    def readNextLine(cls, gitFile):
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
        self.fileName = fileName
        print fileName

    def analyzeGitLogFile(self):
        "Controls the looping through the git file"
        self.gitFile = codecs.open(self.fileName)
        __currAssignmentName = self.originalAssignmentName     # first assignment name
        __myAssignment = Assignment.Assignment(__currAssignmentName)

        GitFile.readNextLine(self.gitFile)                                     # first line says commit
        for line in self.gitFile:
            __nextAssignmentName = __myAssignment.analyzeAssignment(self.gitFile)
            self.myAssignmentsList.append(__myAssignment)
            __myAssignment = Assignment.Assignment(__nextAssignmentName)

        # save last Assignment in the file to Assignments List
        self.myAssignmentsList.append(__myAssignment)
        self.gitFile.close()

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
