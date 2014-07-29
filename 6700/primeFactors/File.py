'''
Created on Jul 24, 2014

@author: susanha
'''
import CommitDetails

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
        self.testFile = testFile
        
    def setCommitDetails(self, commitNbr, addedLines, deletedLines):
        myCommitDetails = CommitDetails.CommitDetails(commitNbr, addedLines, deletedLines)
        self.commitDetails.append(myCommitDetails)

    def getCommitDetails(self):
        return self.commitDetails
        
    def getFileName(self):
        return self.fileName