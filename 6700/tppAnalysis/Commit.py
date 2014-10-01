'''
Created on Jul 24, 2014

@author: susanha
'''


class Commit(object):
    '''
    classdocs
    '''


    def __init__(self,commitNbr, addedLines,deletedLines, testFiles,prodFiles, nbrOfTrans):
        '''
        Constructor
        '''
        self.commitNbr = commitNbr
        self.addedLinesInCommit = addedLines
        self.deletedLinesInCommit = deletedLines
        self.numberOfTransformations = nbrOfTrans
        self.testFiles = testFiles
        self.prodFiles = prodFiles
        self.transformations = []
        
    def getAddedLinesInCommit(self):
        return self.addedLinesInCommit
    
    def addTransformation(self, transformation):
        self.transformations.append(transformation)
        
    def getTransformations(self):
        return self.transformations
    
    def getNbrOfTransformations(self):
        return self.numberOfTransformations