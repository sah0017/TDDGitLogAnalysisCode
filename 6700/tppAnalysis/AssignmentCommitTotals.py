'''
Created on Apr 12, 2016

@author: susanha
'''


class AssignmentCommitTotals(object):
    '''
    classdocs
    '''


    def __init__(self, nbrCommits, redLight, greenLight, nbrRefactor, other, avgLperC, avgTperC, ratio, overallDeletedLines):
        '''
        Constructor
        '''

        #self.assignment = assignment
        self.nbrCommits = nbrCommits
        self.RLCommit = redLight
        self.GLCommit = greenLight
        self.refCommit = nbrRefactor
        self.otherCommit = other
        self.avgLinesPerCommit = avgLperC
        self.avgTransPerCommit = avgTperC
        self.ratioTestToProd = ratio
        self.totalDelLines = overallDeletedLines
    def get_assignment(self):
        return self.__assignment


    def get_nbr_commits(self):
        return self.__nbrCommits


    def get_rlcommit(self):
        return self.__RLCommit


    def get_glcommit(self):
        return self.__GLCommit


    def get_ref_commit(self):
        return self.__refCommit


    def get_other_commit(self):
        return self.__otherCommit


    def get_avg_lines_per_commit(self):
        return self.__avgLinesPerCommit


    def get_avg_trans_per_commit(self):
        return self.__avgTransPerCommit


    def get_ratio_test_to_prod(self):
        return self.__ratioTestToProd


    def get_total_del_lines(self):
        return self.__totalDelLines


    def set_assignment(self, value):
        self.__assignment = value


    def set_nbr_commits(self, value):
        self.__nbrCommits = value


    def set_rlcommit(self, value):
        self.__RLCommit = value


    def set_glcommit(self, value):
        self.__GLCommit = value


    def set_ref_commit(self, value):
        self.__refCommit = value


    def set_other_commit(self, value):
        self.__otherCommit = value


    def set_avg_lines_per_commit(self, value):
        self.__avgLinesPerCommit = value


    def set_avg_trans_per_commit(self, value):
        self.__avgTransPerCommit = value


    def set_ratio_test_to_prod(self, value):
        self.__ratioTestToProd = value


    def set_total_del_lines(self, value):
        self.__totalDelLines = value


    def del_assignment(self):
        del self.__assignment


    def del_nbr_commits(self):
        del self.__nbrCommits


    def del_rlcommit(self):
        del self.__RLCommit


    def del_glcommit(self):
        del self.__GLCommit


    def del_ref_commit(self):
        del self.__refCommit


    def del_other_commit(self):
        del self.__otherCommit


    def del_avg_lines_per_commit(self):
        del self.__avgLinesPerCommit


    def del_avg_trans_per_commit(self):
        del self.__avgTransPerCommit


    def del_ratio_test_to_prod(self):
        del self.__ratioTestToProd


    def del_total_del_lines(self):
        del self.__totalDelLines

    assignment = property(get_assignment, set_assignment, del_assignment, "assignment's docstring")
    nbrCommits = property(get_nbr_commits, set_nbr_commits, del_nbr_commits, "nbrCommits's docstring")
    RLCommit = property(get_rlcommit, set_rlcommit, del_rlcommit, "RLCommit's docstring")
    GLCommit = property(get_glcommit, set_glcommit, del_glcommit, "GLCommit's docstring")
    refCommit = property(get_ref_commit, set_ref_commit, del_ref_commit, "refCommit's docstring")
    otherCommit = property(get_other_commit, set_other_commit, del_other_commit, "otherCommit's docstring")
    avgLinesPerCommit = property(get_avg_lines_per_commit, set_avg_lines_per_commit, del_avg_lines_per_commit, "avgLinesPerCommit's docstring")
    avgTransPerCommit = property(get_avg_trans_per_commit, set_avg_trans_per_commit, del_avg_trans_per_commit, "avgTransPerCommit's docstring")
    ratioTestToProd = property(get_ratio_test_to_prod, set_ratio_test_to_prod, del_ratio_test_to_prod, "ratioTestToProd's docstring")
    totalDelLines = property(get_total_del_lines, set_total_del_lines, del_total_del_lines, "totalDelLines's docstring")
