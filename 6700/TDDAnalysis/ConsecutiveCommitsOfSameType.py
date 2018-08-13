"""
Created on June 2, 2017

@author: susan hammond
"""

import GitFile


class ConsecutiveCommitsOfSameType(object):
    """
    The ConsecutiveCommitsOfSameType object will hold the information when 2 consecutive
    commits are of the same type.  What files were edited?  What information can we intuit
    from this data?
    """

    reasonList = {"Undetermined": 0, "Same test file": 1, "Same prod file": 2, "Multiple Files": 3}

    def getReasonValue(cls, reason_key):
        return cls.reasonList[reason_key]

    def __init__(self, commit_type, commit1, commit2):
        self.consCommitType = commit_type
        self.firstCommitNbr = commit1
        self.firstCommitFileList = []
        self.secondCommitNbr = commit2
        self.secondCommitFileList = []
        self.reason = 0

    def setFirstCommitList(self, file_list):
        self.firstCommitFileList = file_list

    def setSecondCommitList(self, file_list):
        self.secondCommitFileList = file_list

    def reasonForDuplicateTypes(self):
        if len(self.firstCommitFileList) > 1 or len(self.secondCommitFileList) > 1:
            self.reason = self.getReasonValue("Multiple Files")
        elif self.firstCommitFileList[0] == self.secondCommitFileList[0]:
            fileType = GitFile.GitFile.getFileType(self.firstCommitFileList[0])
            if fileType == "Prod":
                self.reason = self.getReasonValue("Same prod file")
            else:
                self.reason = self.getReasonValue("Same test file")
        return self.reason

    def get_commit_type(self):
        return self.consCommitType

    def get_first_commit_nbr(self):
        return self.firstCommitNbr

    def get_second_commit_nbr(self):
        return self.secondCommitNbr
