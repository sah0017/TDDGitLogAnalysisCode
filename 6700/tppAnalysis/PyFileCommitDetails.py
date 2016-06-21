'''
Created on Jul 28, 2014

@author: susanha
'''

class PyFileCommitDetails(object):
    '''
    classdocs
    '''


    def __init__(self, assignmentName, commitNbr, addedLines, deletedLines, taTestLines, methodNames):
        '''
        Constructor
        '''
        self.assignmentName = assignmentName
        self.commitNbr = commitNbr
        self.addedLines = addedLines
        self.deletedLines = deletedLines
        self.taTestLines = taTestLines
        self.methodNames = methodNames
        
    def getCommitDetails(self):
        return [self.assignmentName, self.commitNbr, self.addedLines, self.deletedLines, self.methodNames]