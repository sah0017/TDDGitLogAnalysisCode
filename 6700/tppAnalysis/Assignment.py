'''
Created on Apr 7, 2016

@author: susanha
'''
from datetime import date

class Assignment(object):
    '''
    classdocs
    '''
    TATestCase1 = date(2016,4,6)
    Assignment2Date = date(2016,4,25)
    Assignment3Date = date(2016,5,7)
    assignmentDict = {1:TATestCase1, 2:Assignment2Date, 3:Assignment3Date}

    def __init__(self,assnNbr):
        '''
        Constructor
        '''
        self.assignmentNbr = assnNbr
        self.myCommits = []
        self.myCommitTotals = []

      

    def addCommitToAssignment(self, commit):
        self.myCommits.append(commit)
        
    def addCommitTotalsToAssignment(self, commitTotals):
        self.myCommitTotals.append(commitTotals)
        
    @classmethod
    def get_assignment_dict(self):
        return self.assignmentDict


    def get_assignment_nbr(self):
        return self.__assignmentNbr


    def get_my_commits(self):
        return self.__myCommits


    def get_my_commit_totals(self):
        return self.__myCommitTotals


    def set_assignment_dict(self, value):
        self.__assignmentDict = value


    def set_assignment_nbr(self, value):
        self.__assignmentNbr = value


    def set_my_commits(self, value):
        self.__myCommits = value


    def set_my_commit_totals(self, value):
        self.__myCommitTotals = value


    def del_assignment_dict(self):
        del self.__assignmentDict


    def del_assignment_nbr(self):
        del self.__assignmentNbr


    def del_my_commits(self):
        del self.__myCommits


    def del_my_commit_totals(self):
        del self.__myCommitTotals

    assignmentNbr = property(get_assignment_nbr, set_assignment_nbr, del_assignment_nbr, "assignmentNbr's docstring")
    myCommits = property(get_my_commits, set_my_commits, del_my_commits, "myCommits's docstring")
    myCommitTotals = property(get_my_commit_totals, set_my_commit_totals, del_my_commit_totals, "myCommitTotals's docstring")
        