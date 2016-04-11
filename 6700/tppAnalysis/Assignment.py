'''
Created on Apr 7, 2016

@author: susanha
'''
from datetime import date

class Assignment(object):
    '''
    classdocs
    '''
    assignment1Date = date(2016,4,6)
    assignmentDict = {1:assignment1Date}

    def __init__(self,assnNbr):
        '''
        Constructor
        '''
        self.assignmentNbr = assnNbr
        self.myCommits = []

      

    def addCommitToAssignment(self, commit):
        self.myCommits.append(commit)
        
        
    def getAssignmentDict(self):
        return self.assignmentDict
        