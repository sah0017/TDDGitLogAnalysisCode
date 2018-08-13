"""
Created on Jul 28, 2014

@author: susan hammond
"""


class PyFileCommitDetails(object):
    """    classdocs
    """

    def __init__(self, commit_nbr, added_lines, deleted_lines, ta_test_lines, method_names):
        """
        Constructor
        """
        self.commitNbr = commit_nbr
        self.addedLines = added_lines
        self.deletedLines = deleted_lines
        self.TATestLines = ta_test_lines
        self.methodNames = method_names
        
    def getCommitDetails(self):
        return [self.commitNbr, self.addedLines, self.deletedLines, self.methodNames]
