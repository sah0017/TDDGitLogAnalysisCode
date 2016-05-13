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
        
    def setCommitDetails(self, commitNbr, addedLines, deletedLines, methodNames):
        myCommitDetails = PyFileCommitDetails.PyFileCommitDetails(commitNbr, addedLines, deletedLines, methodNames)
        self.commitDetails.append(myCommitDetails)

    def setMethodName(self, methodName):
        myMethod = Method.Method(methodName,[])
        self.methodNames.append(myMethod)
        
        
    def getCommitDetails(self):
        return self.commitDetails
        
    def extractFileName(self):
        return self.fileName