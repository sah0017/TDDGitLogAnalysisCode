'''
Created on Jul 28, 2014

@author: susanha
'''

class PyFileCommitDetails(object):
    '''
    classdocs
    '''


    def __init__(self, commitNbr, addedLines, deletedLines, taTestLines, methodNames):
        '''
        Constructor
        '''
        self.commitNbr = commitNbr
        self.addedLines = addedLines
        self.deletedLines = deletedLines
        self.TATestLines = taTestLines
        self.methodNames = methodNames
        
    def getCommitDetails(self):
        return [self.commitNbr, self.addedLines, self.deletedLines, self.methodNames]
