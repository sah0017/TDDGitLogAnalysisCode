"""
Created on Jun 23, 2015

@author: susan hammond
"""


class DeletedLine(object):
    """
    classdocs
    """

    def __init__(self, line_content):
        """
        Constructor
        """
        self.lineContent = line_content
        self.deletedIfContents = ""
        self.deletedWhileContents = ""
        self.deletedReturn = False
        self.deletedNullValue = False
        self.deletedLiteral = False
        self.deletedIf = False
        self.deletedWhile = False
        self.deletedVariable = False
        self.deletedVariableName = ""
