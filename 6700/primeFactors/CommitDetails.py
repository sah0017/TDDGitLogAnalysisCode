'''
Created on Jul 28, 2014

@author: susanha
'''

class CommitDetails(object):
    '''
    classdocs
    '''


    def __init__(self, commitNbr, addedLines, deletedLines, methodNames):
        '''
        Constructor
        '''
        self.commitNbr = commitNbr
        self.addedLines = addedLines
        self.deletedLines = deletedLines
        self.methodNames = methodNames
        
    def getCommitDetails(self):
        return [self.commitNbr, self.addedLines, self.deletedLines, self.methodNames]