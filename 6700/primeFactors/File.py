'''
Created on Jul 24, 2014

@author: susanha
'''
import CommitDetails
import Method

class File(object):
    '''
    classdocs
    '''


    def __init__(self, fileName, testFile, commitNbr):
        '''
        Constructor
        '''
        self.fileName = fileName
        self.commitAdded = commitNbr
        self.commitDetails = []
        self.methodNames = []
        self.testFile = testFile
        
    def setCommitDetails(self, commitNbr, addedLines, deletedLines, methodNames):
        myCommitDetails = CommitDetails.CommitDetails(commitNbr, addedLines, deletedLines, methodNames)
        self.commitDetails.append(myCommitDetails)

    def setMethodName(self, methodName):
        myMethod = Method.Method(methodName)
        self.methodNames.append(myMethod)
        
        
    def getCommitDetails(self):
        return self.commitDetails
        
    def extractFileName(self):
        return self.fileName