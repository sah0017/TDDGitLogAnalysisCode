'''
Created on June 6, 2017

@author: susanha
'''

import GitFile
import Assignment
import Commit
import os

class TDDCycle(object):
    '''
    The TDDCycle object will collect the various pieces of data about the TDD Cycle itself.
    Will result in data to be used in determining process conformance.
    '''

    def __init__(self, startsWithRL):
        self.startsWithRL = startsWithRL
        self.validCommit = []
        self.CommitTypes = []       # will contain a list of commit types in the TDD Cycle
        self.transformations = []   # this will be a list of lists; the indexed values of
                                    # transformation lists will correspond with the same
                                    # index in the commit type list

    def addCommit(self, commit):
        self.CommitTypes.append(commit.get_commit_type())
        transList = commit.get_transformations()
        for tr in transList:
            self.transformations.append(tr)
        self.validCommit.append(commit.get_commit_validity())

    def too_many_trans(self):
        nbrCommitsTooManyTrans = 0
        for tr in self.transformations:
            if len(tr) > 1:
                nbrCommitsTooManyTrans += 1
        if nbrCommitsTooManyTrans > 0:
            return True
        else:
            return False

    def invalid_commits(self):
        nbrInvalidCommits = 0
        for vc in self.validCommit:
            if vc == "INVALID":
                nbrInvalidCommits += 1
        if nbrInvalidCommits > 0:
            return True
        else:
            return False

    def is_cycle_valid(self):
        if self.too_many_trans() or self.invalid_commits():
            return False
        else:
            return True
