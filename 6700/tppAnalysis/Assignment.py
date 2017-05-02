'''
Created on Apr 7, 2016

@author: susanha
'''
import time
import ConfigParser



class Assignment(object):
    '''
    classdocs
    '''
    '''
    Assignment3 = date(2017,3,20)
    Assignment4 = date(2017,3,27)

    assignmentNameDict = {Assignment3:"Assignment3", Assignment4:"Assignment4"}
    '''
    @classmethod
    def loadAssignments(self):
        myConfig = ConfigParser.SafeConfigParser() 
        myConfig.read("TDDanalysis.cfg")
        self.myFirstAssignment = myConfig.get("Assignments","BaseName") + myConfig.get("Assignments","FirstTDDAssignment")
        self.assignmentNameDict = {}
        for key, val in myConfig.items("Due Dates"):
            self.assignmentNameDict[key] = time.strptime(val,"%Y, %m, %d")
        #print self.assignmentNameDict
    
    @classmethod
    def getMyFirstAssignment(self):
        return self.myFirstAssignment   
    
    @classmethod
    def get_assignment_name_dict(self):
        return self.assignmentNameDict

    def __init__(self,assnName):
        '''
        Constructor
        '''
        self.assignmentName = assnName
        self.myCommits = []
        self.myCommitTotals = []
      


    def addCommitToAssignment(self, commit):
        self.myCommits.append(commit)
        
    def addCommitTotalsToAssignment(self, commitTotals):
        self.myCommitTotals.append(commitTotals)
    


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

    assignmentName = property(get_assignment_nbr, set_assignment_nbr, del_assignment_nbr, "assignmentName's docstring")
    myCommits = property(get_my_commits, set_my_commits, del_my_commits, "myCommits's docstring")
    myCommitTotals = property(get_my_commit_totals, set_my_commit_totals, del_my_commit_totals, "myCommitTotals's docstring")


if __name__ == "__main__":
    Assignment.loadAssignments()
    
        