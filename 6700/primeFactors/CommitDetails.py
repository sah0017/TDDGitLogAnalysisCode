'''
Created on Jul 28, 2014

@author: susanha
'''

class CommitDetails(object):
    '''
    classdocs
    '''


    def __init__(self, commitNbr, addedLines, deletedLines):
        '''
        Constructor
        '''
        self.commitNbr = commitNbr
        self.addedLines = addedLines
        self.deletedLines = deletedLines
        
    def getCommitDetails(self):
        return [self.commitNbr, self.addedLines, self.deletedLines]