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
        self.TATestLines = 0
        self.TATestCase = False
        
        
    def setDeletedReturnValue(self, RtnValue):
        self.deletedReturnValue = RtnValue
        
    def addDeletedLine(self, deletedLines):
        self.deletedLines.append(deletedLines)
        
    def getDeletedReturnValue(self):
        return self.deletedReturnValue
        
    def getDeletedLines(self):
        return len(self.deletedLines)   
    
    def getAddedLines(self):
        addedLines = self.addedLines - self.TATestLines
        if addedLines < 0:
            return 0
        return addedLines 
    
    def updateTATestLines(self, TATestLOC):
        self.TATestLines = self.TATestLines + TATestLOC
        
    def setIsTATestCase(self, isTATestCase):
        self.TATestCase = isTATestCase
        
    def isATATestCase(self):
        return self.TATestCase