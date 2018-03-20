'''
Created on Jul 24, 2014

@author: susanha

Used by:  Assignment
At a class level, contains the total statistics for a particular commit.
Parameters:  None

Results:  analyzes a specific commit within an assignment within a git file and tracks data about it.
Also evaluates whether the commit is valid or invalid.
A commit may contain references to multiple python files.  The commit contains a list of PyFile objects.
Uses:  PyFile


'''

import PyFile
import Transformations
import FileHandler
import GitFile

class Commit(object):
    '''
    The Commit object will hold the total statistics for a particular commit, including
    a list of the files added/modified in the commit.
    '''

    @classmethod
    def foundNewCommit(cls, line):
        " Are we still in the same commit or is this a new one? "
        if line.startswith("\"commit"):   ## using this key word in the commit comment line to find the next commit
            return True
        elif line == '':   ## looking for end of file
            return True
        else:
            return False

    def __init__(self, commitNbr, fileIOobject):
        '''
        Constructor
        '''
        self.commitNbr = commitNbr
        line = fileIOobject.readNextLine()             # advance to next line to get commit type
        self.commitType = line.strip().rstrip("\"|")
        fileIOobject.readNextLine()         # advance to next line to get the first file name in the commit
        self.addedLinesInCommit = 0
        self.deletedLinesInCommit = 0
        self.addedTestLOC = 0
        self.addedTATestLOC = 0
        self.deletedTestLOC = 0
        self.numberOfTransformations = 0
        self.nbrTestFiles = 0
        self.nbrProdFiles = 0
        self.transformations = []
        self.commitValidity = 'Valid'
        self.myFiles = []       # a list of pyFile objects for this commit

    def set_commit_validity(self, commit_type):
        # if it's a Green Light, they worked on a prod file.  Red Light worked on a test file.
        if commit_type == "Green Light":
            if (self.addedTestLOC > 0) or (self.deletedTestLOC > 0) or self.nbrTestFiles > 0:
                self.commitValidity = 'INVALID'
        elif commit_type == "Red Light":
            if (self.addedLinesInCommit > 0) or (self.deletedLinesInCommit > 0) or self.nbrProdFiles > 0:
                self.commitValidity = 'INVALID'
        elif commit_type != "Refactor":
            self.commitValidity = "INVALID"
        return self.commitValidity

    def has_too_many_files_in_commit(self):
        nbrFiles = self.nbrTestFiles + self.nbrProdFiles
        if nbrFiles > 1:
            return True
        return False

    def analyzeCommit(self, gitFileHandle, line):
        "Analyzes all the lines in an individual commit"

        #self.commitType = self.readCommitType(gitFileHandle)
        #for line in gitFileHandle:
        while Commit.foundNewCommit(gitFileHandle.getCurrentLine()) == False:
            line = gitFileHandle.getCurrentLine()
            if PyFile.PyFile.pythonFileFound(line):
                path, fileName = PyFile.PyFile.extractFileName(line)
                fileIndex = self.findExistingFileToAddCommitDetails(fileName)
                if fileIndex == -1:
                    myPyFile = self.addNewFile(path, fileName, self.commitNbr, gitFileHandle)


                myPyFileCommitDetails = myPyFile.analyzePyFile(gitFileHandle)
                if myPyFile.isProdFile():
                    self.increment_nbr_prod_files()
                    self.add_added_lines_in_commit(myPyFileCommitDetails.addedLines)
                    self.add_deleted_lines_in_commit(myPyFileCommitDetails.deletedLines)
                else:
                    self.increment_nbr_test_files()
                    self.add_added_test_loc(myPyFileCommitDetails.addedLines)
                    self.add_deleted_test_loc(myPyFileCommitDetails.deletedLines)
                    self.set_added_tatest_loc(myPyFileCommitDetails.TATestLines)
                self.add_number_of_transformations(myPyFile.numberOfTransformationsInPyFile())

                self.addTransformation(myPyFile.get_transformations())

            else:
                line = gitFileHandle.readNextLine()

        return self

    def addNewFile(self, path, fileName, commitNbr, gitFileHandle):
        " This is a new file that isn't in our analysis yet. "
        newFile = PyFile.PyFile(path, fileName, commitNbr)
        self.myFiles.append(newFile)
        if GitFile.GitFile.newPyFile(fileName):
            newFile.addToTransformationList(Transformations.Trans.getTransValue("NEWFILE"))
            GitFile.GitFile.addNewPyFile(newFile)
        line = gitFileHandle.readNextLine() ## if this was a new file, then advance file pointer to index line
        return newFile

    def findExistingFileToAddCommitDetails(self, fileName):
        fileIndex = -1
        for x in self.myFiles:
            if x.getFileName() == fileName:
                fileIndex = self.myFiles.index(x)

        return fileIndex

    def get_added_tatest_loc(self):
        return self.__addedTATestLOC

    def set_added_tatest_loc(self, value):
        self.__addedTATestLOC = value

    def del_added_tatest_loc(self):
        del self.__addedTATestLOC

    def addTransformation(self, transformation):
        self.transformations.append(transformation)

    def get_commit_nbr(self):
        return self.__commitNbr

    def get_commit_type(self):
        if self.commitType.startswith("Red Light"):
            ct = "Red Light"
        elif self.commitType.startswith("Green Light"):
            ct = "Green Light"
        elif self.commitType.startswith("Refactor"):
            ct = "Refactor"
        else:
            ct = "Other"
        if self.nbrTestFiles == 0 and self.nbrProdFiles == 0:
            ct = "No Python Code"
        return ct

    def get_commit_validity(self):
        return self.commitValidity

    def get_file_list(self):
        return self.myFiles

    def get_file_names_list(self):
        fileNamesList = []
        for f in self.myFiles:
            fileNamesList.append(f.getFileName())   # only need the name, not the whole pyFile object
        return fileNamesList

    def get_added_lines_in_commit(self):
        return self.__addedLinesInCommit

    def get_deleted_lines_in_commit(self):
        return self.__deletedLinesInCommit

    def get_added_test_loc(self):
        return self.__addedTestLOC

    def get_deleted_test_loc(self):
        return self.__deletedTestLOC

    def get_number_of_transformations(self):
        return self.numberOfTransformations

    def get_nbr_test_files(self):
        return self.__nbrTestFiles

    def get_nbr_prod_files(self):
        return self.__nbrProdFiles

    def get_transformations(self):
        return self.transformations

    def set_commit_nbr(self, value):
        self.__commitNbr = value

    def set_commit_type(self, value):
        self.__commitType = value

    def set_added_lines_in_commit(self, value):
        self.__addedLinesInCommit = value

    def add_added_lines_in_commit(self, value):
        self.__addedLinesInCommit = self.__addedLinesInCommit + value

    def set_deleted_lines_in_commit(self, value):
        self.__deletedLinesInCommit = value

    def add_deleted_lines_in_commit(self, value):
        self.__deletedLinesInCommit = self.__deletedLinesInCommit + value

    def set_added_test_loc(self, value):
        self.__addedTestLOC = value

    def add_added_test_loc(self, value):
        self.__addedTestLOC = self.__addedTestLOC + value

    def set_deleted_test_loc(self, value):
        self.__deletedTestLOC = value

    def add_deleted_test_loc(self, value):
        self.__deletedTestLOC = self.__deletedTestLOC + value

    def set_number_of_transformations(self, value):
        self.__numberOfTransformations = value

    def add_number_of_transformations(self, value):
        self.numberOfTransformations = self.numberOfTransformations + value

    def set_nbr_test_files(self, value):
        self.__nbrTestFiles = value

    def increment_nbr_test_files(self):
        self.__nbrTestFiles += 1

    def set_nbr_prod_files(self, value):
        self.__nbrProdFiles = value

    def increment_nbr_prod_files(self):
        self.__nbrProdFiles += 1

    def set_transformations(self, value):
        self.transformations.append(value)

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

    #def del_transformations(self):
    #    del self.__transformations

    commitNbr = property(get_commit_nbr, set_commit_nbr, del_commit_nbr, "commitNbr's docstring")
    #commitType = property(get_commit_type, set_commit_type, del_commit_type, "commitType's docstring")
    addedLinesInCommit = property(get_added_lines_in_commit, set_added_lines_in_commit, del_added_lines_in_commit, "addedLinesInCommit's docstring")
    deletedLinesInCommit = property(get_deleted_lines_in_commit, set_deleted_lines_in_commit, del_deleted_lines_in_commit, "deletedLinesInCommit's docstring")
    addedTestLOC = property(get_added_test_loc, set_added_test_loc, del_added_test_loc, "addedTestLOC's docstring")
    deletedTestLOC = property(get_deleted_test_loc, set_deleted_test_loc, del_deleted_test_loc, "deletedTestLOC's docstring")
    nbrTestFiles = property(get_nbr_test_files, set_nbr_test_files, del_nbr_test_files, "nbrTestFiles's docstring")
    nbrProdFiles = property(get_nbr_prod_files, set_nbr_prod_files, del_nbr_prod_files, "nbrProdFiles's docstring")
    addedTATestLOC = property(get_added_tatest_loc, set_added_tatest_loc, del_added_tatest_loc, "addedTATestLOC's docstring")
