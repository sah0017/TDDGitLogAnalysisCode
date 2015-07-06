'''
Created on Aug 6, 2014

@author: susanha
'''

class Method(object):
    '''
    classdocs
    '''


    def __init__(self, methodName, parameters):
        '''
        Constructor
        '''
        self.methodName = methodName
        self.parameters = parameters
        self.deletedReturnValue = None
        self.deletedLines = []
        self.addedLines = 0
        
        
    def setDeletedReturnValue(self, RtnValue):
        self.deletedReturnValue = RtnValue
        
    def addDeletedLine(self, deletedLines):
        self.deletedLines.append(deletedLines)
        
    def getDeletedReturnValue(self):
        return self.deletedReturnValue
        
    def getDeletedLines(self):
        return self.deletedLines    