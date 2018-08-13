"""
Created on Aug 6, 2014

@author: susan hammond
"""


class Method(object):
    """
    classdocs
    """

    def __init__(self, method_name, parameters):
        """
        Constructor
        """
        self.methodName = method_name
        self.parameters = parameters
        self.deletedReturnValue = None
        self.deletedLines = []
        self.addedLines = 0
        self.TATestLines = 0
        self.TATestCase = False

    def setMethodName(self,method_name):
        self.methodName = method_name
        
    def setDeletedReturnValue(self, rtn_value):
        self.deletedReturnValue = rtn_value
        
    def addDeletedLine(self, deleted_lines):
        self.deletedLines.append(deleted_lines)
        
    def getDeletedReturnValue(self):
        return self.deletedReturnValue
        
    def getDeletedLines(self):
        return len(self.deletedLines)   
    
    def getTATestLines(self):
        return self.TATestLines
    
    def getAddedLines(self):
        added_lines = self.addedLines - self.TATestLines
        if added_lines < 0:
            return 0
        return added_lines
    
    def updateTATestLines(self, t_a_test_l_o_c):
        self.TATestLines = self.TATestLines + t_a_test_l_o_c
        
    def setIsTATestCase(self, is_t_a_test_case):
        self.TATestCase = is_t_a_test_case
        
    def isATATestCase(self):
        return self.TATestCase
