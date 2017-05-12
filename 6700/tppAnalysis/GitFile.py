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

        self.myAssignmentsList = []         # a list of all the Assignment instances in this file
        self.fileName = fileName
        print fileName

    def analyzeGitLogFile(self):
        "Controls the looping through the git file"
        self.gitFile = codecs.open(self.fileName)
        __currAssignmentName = self.originalAssignmentName     # first assignment name
        __myAssignment = Assignment.Assignment(__currAssignmentName)

        GitFile.readNextLine(self.gitFile)                                     # first line says commit
        for line in self.gitFile:
            __nextAssignmentName = __myAssignment.analyzeAssignment(self.gitFile)   # reads thru file until it hits a new assignment
            self.myAssignmentsList.append(__myAssignment)
            __myAssignment = Assignment.Assignment(__nextAssignmentName)

        # save last Assignment in the file to Assignments List
        self.myAssignmentsList.append(__myAssignment)
        self.gitFile.close()

    def GenerateInvididualReport(self, path, fileName):
        # list containing PyFile objects with file name and relevant data
        myFiles = []
        # list containing all the assignments, which contains a list of all the commits in that assignment
        myAssignments = self.getAssignments()
        outFile = open(path + os.sep + fileName + ".gitout", "w")
        outFile.write("Assignments in log file:  " + str(len(myAssignments)))
        for myAssignment in myAssignments:
            myCommitStats = myAssignment.CalculateMyCommitStats(outFile)
            myAssignment.addCommitTotalsToAssignment(myCommitStats)
            myFiles = self.getFiles(myAssignment)
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

        outFile.close()

    def getAssignments(self):
        return self.myAssignmentsList

    def setAssignments(self,assignmentList):
        self.myAssignmentsList = assignmentList

    def getFiles(self, myAssignment):
        myFiles = myAssignment.getFiles()
        return myFiles
    
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
