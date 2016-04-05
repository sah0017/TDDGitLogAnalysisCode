'''
Created on Jun 23, 2015

@author: susanha
'''

class DeletedLine(object):
    '''
    classdocs
    '''


    def __init__(self, lineContent):
        '''
        Constructor
        '''
        self.lineContent = lineContent
        self.deletedIfContents = ""
        self.deletedWhileContents = ""
        self.deletedReturn = False
        self.deletedNullValue = False
        self.deletedLiteral = False
        self.deletedIf = False
        self.deletedWhile = False