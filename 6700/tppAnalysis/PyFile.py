'''
Created on Jul 24, 2014

@author: susanha
'''
import PyFileCommitDetails
import Method

class PyFile(object):
    '''
    classdocs
    '''


    def __init__(self, fileName, prodFile, commitNbr):
        '''
        Constructor
        '''
        self.fileName = fileName
        self.nbrOfCommits = commitNbr
        self.commitDetails = []
        self.methods = []
        self.prodFile = prodFile
        
    def setCommitDetails(self, assignmentName, commitNbr, addedLines, deletedLines, taTestLines, methodNames):
        myCommitDetails = PyFileCommitDetails.PyFileCommitDetails(assignmentName, commitNbr, addedLines, deletedLines, taTestLines, methodNames)
        self.commitDetails.append(myCommitDetails)

    def setMethodName(self, methodName):
        myMethod = Method.Method(methodName,[])
        self.methodNames.append(myMethod)
        
        
    def getCommitDetails(self):
        return self.commitDetails
        
    def extractFileName(self):
        return self.fileName