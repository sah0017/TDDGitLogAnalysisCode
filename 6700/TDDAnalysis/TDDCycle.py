"""
Created on June 6, 2017

@author: susan hammond

Used by:  Assignment
Collects info about the overall TDD Cycle.
Parameters:  when instantiated, receives a boolean value indicating whether or not this cycle began with a Red Light.
Results:  Contain the code that analyzes the TPP transformations in the commit.
Uses:
"""


class TDDCycle(object):

    """
    The TDDCycle object will collect the various pieces of data about the TDD Cycle itself.
    Will result in data to be used in determining process conformance.
    """

    def __init__(self, starts_with_r_l):
        self.startsWithRL = starts_with_r_l
        self.validCommit = []
        self.CommitTypes = []       # will contain a list of commit types in the TDD Cycle
        self.transformations = []   # this will be a list of lists; the indexed values of
                                    # transformation lists will correspond with the same
                                    # index in the commit type list

    def addCommit(self, commit):
        self.CommitTypes.append(commit.get_commit_type())
        trans_list = commit.get_transformations()
        for tr in trans_list:
            self.transformations.append(tr)
        self.validCommit.append(commit.get_commit_validity())

    def too_many_trans(self):
        nbr_commits_too_many_trans = 0
        for tr in self.transformations:
            if len(tr) > 1:
                nbr_commits_too_many_trans += 1
        if nbr_commits_too_many_trans > 0:
            return True
        else:
            return False

    def invalid_commits(self):
        nbr_invalid_commits = 0
        for vc in self.validCommit:
            if vc == "INVALID":
                nbr_invalid_commits += 1
        if nbr_invalid_commits > 0:
            return True
        else:
            return False

    def is_cycle_valid(self):
        if self.too_many_trans() or self.invalid_commits():
            return False
        else:
            return True
