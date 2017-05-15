'''
Created on Jul 24, 2014

@author: susanha
'''

import PyFile
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

    @classmethod
    def readCommitType(self, gitFileHandle):
        line = gitFileHandle.readNextLine()             # advance to next line to get commit type
        commitType = line.strip().rstrip("\"|")
        gitFileHandle.readNextLine()         # advance to next line to get the first file name in the commit
        return commitType

    def __init__(self, assignmentName, commitNbr, commitType):
        '''
        Constructor
        '''
        self.assignmentName = assignmentName
        self.commitNbr = commitNbr
        self.commitType = commitType
        self.addedLinesInCommit = 0
        self.deletedLinesInCommit = 0
        self.addedTestLOC = 0
        self.addedTATestLOC = 0
        self.deletedTestLOC = 0
        self.numberOfTransformations = 0
        self.nbrTestFiles = 0
        self.nbrProdFiles = 0
        #self.transformations = []
        self.validCommit = True
        self.myFiles = []       # a list of pyFile objects for this commit

    def is_valid_gl_commit(self):
        # if it's a Green Light, they worked on a prod file.  Red Light worked on a test file.
        validCommit = True

        if self.get_commit_type() == "Green Light":
            if (self.addedTestLOC > 0) or (self.deletedTestLOC > 0):
                validCommit = False

        return validCommit

    def is_valid_rl_commit(self):
        validCommit = True
        if self.get_commit_type() == "Red Light":
            if (self.addedLinesInCommit > 0) or (self.deletedLinesInCommit > 0):
                validCommit = False

        return validCommit

    def has_too_many_files_in_commit(self):
        if self.commitType.startswith("Green Light") and self.nbrProdFiles > 1:
            return True
        if self.commitType.startswith("Red Light") and self.nbrTestFiles > 1:
            return True
        return False

    def analyzeCommit(self, gitFileHandle, line):
        "Analyzes all the lines in an individual commit"

        #self.commitType = self.readCommitType(gitFileHandle)
        #for line in gitFileHandle:
        while Commit.foundNewCommit(line) == False:
            if PyFile.PyFile.pythonFileFound(line):
                path, fileName = PyFile.PyFile.extractFileName(line)
                fileIndex = self.findExistingFileToAddCommitDetails(fileName)
                if fileIndex == -1:
                    myPyFile, fileIndex = self.addNewFile(fileName, self.commitNbr, gitFileHandle)


                myPyFileCommitDetails = myPyFile.analyzePyFile(path,self.assignmentName,
                                                                    gitFileHandle)
                if myPyFile.isProdFile():
                    self.increment_nbr_prod_files()
                    self.add_added_lines_in_commit(myPyFileCommitDetails.addedLines)
                    self.add_deleted_lines_in_commit(myPyFileCommitDetails.deletedLines)
                else:
                    self.increment_nbr_test_files()
                    self.add_added_test_loc(myPyFileCommitDetails.addedLines)
                    self.add_deleted_test_loc(myPyFileCommitDetails.deletedLines)
                    self.set_added_tatest_loc(myPyFileCommitDetails.TATestLines)

            else:
                line = gitFileHandle.readNextLine()
                if line == False:
                    line = ''

        try:
            self.add_number_of_transformations(myPyFile.numberOfTransformationsInPyFile())

            self.set_transformations(myPyFile.getTransformations())
        except:
            pass

        return self

    def addNewFile(self, fileName, commitNbr, gitFileHandle):
        " This is a new file that isn't in our analysis yet. "
        newFile = PyFile.PyFile(fileName, commitNbr)
        self.myFiles.append(newFile)
        newFile.addToTransformationList(PyFile.PyFile.myTrans.NEWFILE)
        self.line = gitFileHandle.readNextLine() ## if this was a new file, then advance file pointer to index line
        fileIndex = len(self.myFiles) - 1
        return newFile, fileIndex

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
        return ct


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
        self.__numberOfTransformations = self.__numberOfTransformations + value

    def set_nbr_test_files(self, value):
        self.__nbrTestFiles = value

    def increment_nbr_test_files(self):
        self.__nbrTestFiles =+ 1

    def set_nbr_prod_files(self, value):
        self.__nbrProdFiles = value

    def increment_nbr_prod_files(self):
        self.__nbrProdFiles =+ 1

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
    addedTATestLOC = property(get_added_tatest_loc, set_added_tatest_loc, del_added_tatest_loc, "addedTATestLOC's docstring")
