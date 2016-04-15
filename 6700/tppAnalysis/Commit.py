'''
Created on Jul 24, 2014

@author: susanha
'''


class Commit(object):
    '''
    classdocs
    '''


    def __init__(self,commitNbr, commitType, addedLines,deletedLines, addedTestLines, deletedTestLines, testFiles,prodFiles, nbrOfTrans):
        '''
        Constructor
        '''
        self.commitNbr = commitNbr
        self.commitType = commitType
        self.addedLinesInCommit = addedLines
        self.deletedLinesInCommit = deletedLines
        self.addedTestLOC = addedTestLines
        self.deletedTestLOC = deletedTestLines
        self.numberOfTransformations = nbrOfTrans
        self.nbrTestFiles = testFiles
        self.nbrProdFiles = prodFiles
        self.transformations = []
        
        
    def addTransformation(self, transformation):
        self.transformations.append(transformation)
        

    def get_commit_nbr(self):
        return self.__commitNbr


    def get_commit_type(self):
        return self.__commitType


    def get_added_lines_in_commit(self):
        return self.__addedLinesInCommit


    def get_deleted_lines_in_commit(self):
        return self.__deletedLinesInCommit


    def get_added_test_loc(self):
        return self.__addedTestLOC


    def get_deleted_test_loc(self):
        return self.__deletedTestLOC


    def get_number_of_transformations(self):
        return self.__numberOfTransformations


    def get_nbr_test_files(self):
        return self.__nbrTestFiles


    def get_nbr_prod_files(self):
        return self.__nbrProdFiles


    def get_transformations(self):
        return self.__transformations


    def set_commit_nbr(self, value):
        self.__commitNbr = value


    def set_commit_type(self, value):
        self.__commitType = value


    def set_added_lines_in_commit(self, value):
        self.__addedLinesInCommit = value


    def set_deleted_lines_in_commit(self, value):
        self.__deletedLinesInCommit = value


    def set_added_test_loc(self, value):
        self.__addedTestLOC = value


    def set_deleted_test_loc(self, value):
        self.__deletedTestLOC = value


    def set_number_of_transformations(self, value):
        self.__numberOfTransformations = value


    def set_nbr_test_files(self, value):
        self.__nbrTestFiles = value


    def set_nbr_prod_files(self, value):
        self.__nbrProdFiles = value


    def set_transformations(self, value):
        self.__transformations = value


    def del_commit_nbr(self):
        del self.__commitNbr


    def del_commit_type(self):
        del self.__commitType


    def del_added_lines_in_commit(self):
        del self.__addedLinesInCommit


    def del_deleted_lines_in_commit(self):
        del self.__deletedLinesInCommit


    def del_added_test_loc(self):
        del self.__addedTestLOC


    def del_deleted_test_loc(self):
        del self.__deletedTestLOC


    def del_number_of_transformations(self):
        del self.__numberOfTransformations


    def del_nbr_test_files(self):
        del self.__nbrTestFiles


    def del_nbr_prod_files(self):
        del self.__nbrProdFiles


    def del_transformations(self):
        del self.__transformations

    commitNbr = property(get_commit_nbr, set_commit_nbr, del_commit_nbr, "commitNbr's docstring")
    commitType = property(get_commit_type, set_commit_type, del_commit_type, "commitType's docstring")
    addedLinesInCommit = property(get_added_lines_in_commit, set_added_lines_in_commit, del_added_lines_in_commit, "addedLinesInCommit's docstring")
    deletedLinesInCommit = property(get_deleted_lines_in_commit, set_deleted_lines_in_commit, del_deleted_lines_in_commit, "deletedLinesInCommit's docstring")
    addedTestLOC = property(get_added_test_loc, set_added_test_loc, del_added_test_loc, "addedTestLOC's docstring")
    deletedTestLOC = property(get_deleted_test_loc, set_deleted_test_loc, del_deleted_test_loc, "deletedTestLOC's docstring")
    numberOfTransformations = property(get_number_of_transformations, set_number_of_transformations, del_number_of_transformations, "numberOfTransformations's docstring")
    nbrTestFiles = property(get_nbr_test_files, set_nbr_test_files, del_nbr_test_files, "nbrTestFiles's docstring")
    nbrProdFiles = property(get_nbr_prod_files, set_nbr_prod_files, del_nbr_prod_files, "nbrProdFiles's docstring")
    transformations = property(get_transformations, set_transformations, del_transformations, "transformations's docstring")
