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
        self.CommitTypes.append(commit.commitType)
        self.transformations.append(commit.transformations)
        self.validCommit.append(commit.validCommit)

    def too_many_trans(self):
        nbrCommitsTooManyTrans = 0
        for tr in self.transformations:
            if len(tr) > 1:
                nbrCommitsTooManyTrans += 1
        return nbrCommitsTooManyTrans

    def get_cycle_validity(self):
        nbrInvalidCycles = 0
        for vc in self.validCommit:
            if not vc:
                nbrInvalidCycles += 1
        return nbrInvalidCycles
