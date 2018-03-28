"""
Created on Jul 24, 2014

@author: susanha

Used by:  Assignment
At a class level, contains the total statistics for a particular commit.
Parameters:  None

Results:  analyzes a specific commit within an assignment within a git file and tracks data about it.
Also evaluates whether the commit is valid or invalid.
A commit may contain references to multiple python files.  The commit contains a list of PyFile objects.
Uses:  PyFile
"""

import PyFile
import Transformations
import FileHandler
import GitFile
import ConfigParser

class Commit(object):
    """
    The Commit object will hold the total statistics for a particular commit, including
    a list of the files added/modified in the commit.
    """
    REDLIGHT = "Red Light"
    GREENLIGHT = "Green Light"
    REFACTOR = "Refactor"
    OTHER = "Other"
    NOPYCODE = "No Python Code"
    LGCOMMITSIZE = 100
    invalid_reason_list = ["undetermined", "redlightwithprodcode", "greenlightwithtestcode",
                           "onetransformation", "largecommit"]

    @classmethod
    def load_recommendations(cls):
        my_config = ConfigParser.SafeConfigParser()
        my_config.read("TDDanalysis.cfg")
        cls.LGCOMMITSIZE = int(my_config.get("Recommendations","LargeCommitSize"))

    @classmethod
    def foundNewCommit(cls, line):
        """ Are we still in the same commit or is this a new one? """
        if line.startswith("\"commit"):     # using this key word in the commit comment line to find the next commit
            return True
        elif line == '':                    # looking for end of file
            return True
        else:
            return False

    def __init__(self, commit_nbr, file_io_object):
        """
        Constructor
        """
        self.commit_nbr = commit_nbr
        line = file_io_object.readNextLine()             # advance to next line to get commit type
        self.commitType = line.strip().rstrip("\"|")
        file_io_object.readNextLine()         # advance to next line to get the first file name in the commit
        self.added_lines_in_commit = 0
        self.deleted_lines_in_commit = 0
        self.added_test_loc = 0
        self.added_ta_test_loc = 0
        self.deleted_test_loc = 0
        self.number_of_transformations = 0
        self.nbr_test_files = 0
        self.nbr_prod_files = 0
        self.transformations = []
        self.commit_validity = 'Valid'
        self.reason = []
        self.my_files = []       # a list of pyFile objects for this commit

    def set_commit_validity(self, commit_type):
        # if it's a Green Light, they should have worked on a prod file.  Red Light worked on a test file.
        if commit_type == Commit.GREENLIGHT:
            if (self.added_test_loc > 0) or (self.deleted_test_loc > 0) or self.nbr_test_files > 0:
                self.commit_validity = 'INVALID'
                #self.reason.append(Commit.invalid_reason_list[2])   omitting green light with prod code for now 3/27/18
        elif commit_type == Commit.REDLIGHT:
            if (self.added_lines_in_commit > 0) or (self.deleted_lines_in_commit > 0) or self.nbr_prod_files > 0:
                self.commit_validity = 'INVALID'
                self.reason.append(Commit.invalid_reason_list[1])
        elif commit_type == Commit.OTHER:
            self.commit_validity = "INVALID"
        """           omitting one transformation per commit for now 3/27/18
        if self.number_of_transformations > 1:
            self.reason.append(Commit.invalid_reason_list[3])  
        """
        if self.added_lines_in_commit + self.added_test_loc > Commit.LGCOMMITSIZE:
            self.reason.append(Commit.invalid_reason_list[4])

    def get_invalid_reason(self):
        return self.reason

    def has_too_many_files_in_commit(self):
        nbr_files = self.nbr_test_files + self.nbr_prod_files
        if nbr_files > 1:
            return True
        return False

    def analyzeCommit(self, git_file_handle, line):
        """
        Analyzes all the lines in an individual commit
        """

        # self.commitType = self.readCommitType(git_file_handle)
        # for line in git_file_handle:
        while Commit.foundNewCommit(git_file_handle.getCurrentLine()) == False:
            line = git_file_handle.getCurrentLine()
            if PyFile.PyFile.pythonFileFound(line):
                path, file_name = PyFile.PyFile.extractFileName(line)
                file_index = self.findExistingFileToAddCommitDetails(file_name)
                if file_index == -1:
                    my_pyfile = self.addnew_file(path, file_name, self.commit_nbr, git_file_handle)


                my_pyfileCommitDetails = my_pyfile.analyzePyFile(git_file_handle)
                if my_pyfile.isProdFile():
                    self.increment_nbr_prod_files()
                    self.add_added_lines_in_commit(my_pyfileCommitDetails.addedLines)
                    self.add_deleted_lines_in_commit(my_pyfileCommitDetails.deletedLines)
                else:
                    self.increment_nbr_test_files()
                    self.add_added_test_loc(my_pyfileCommitDetails.addedLines)
                    self.add_deleted_test_loc(my_pyfileCommitDetails.deletedLines)
                    self.set_added_tatest_loc(my_pyfileCommitDetails.TATestLines)
                self.add_number_of_transformations(my_pyfile.numberOfTransformationsInPyFile())

                self.addTransformation(my_pyfile.get_transformations())

            else:
                line = git_file_handle.readNextLine()

        return self

    def addnew_file(self, path, file_name, commit_nbr, git_file_handle):
        " This is a new file that isn't in our analysis yet. "
        new_file = PyFile.PyFile(path, file_name, commit_nbr)
        self.my_files.append(new_file)
        if GitFile.GitFile.newPyFile(file_name):
            new_file.addToTransformationList(Transformations.Trans.getTransValue("NEWFILE"))
            GitFile.GitFile.addNewPyFile(new_file)
        line = git_file_handle.readNextLine() ## if this was a new file, then advance file pointer to index line
        return new_file

    def findExistingFileToAddCommitDetails(self, file_name):
        file_index = -1
        for x in self.my_files:
            if x.getFileName() == file_name:
                file_index = self.my_files.index(x)

        return file_index

    def get_added_tatest_loc(self):
        return self.__added_ta_test_loc

    def set_added_tatest_loc(self, value):
        self.__added_ta_test_loc = value

    def del_added_tatest_loc(self):
        del self.__added_ta_test_loc

    def addTransformation(self, transformation):
        self.transformations.append(transformation)

    def get_commit_nbr(self):
        return self.__commit_nbr

    def get_commit_type(self):
        if self.commitType.startswith(Commit.REDLIGHT):
            ct = Commit.REDLIGHT
        elif self.commitType.startswith(Commit.GREENLIGHT):
            ct = Commit.GREENLIGHT
        elif self.commitType.startswith(Commit.REFACTOR):
            ct = Commit.REFACTOR
        else:
            ct = Commit.OTHER
        if self.nbr_test_files == 0 and self.nbr_prod_files == 0:
            ct = Commit.NOPYCODE
        return ct

    def get_commit_validity(self):
        return self.commit_validity

    def get_file_list(self):
        return self.my_files

    def get_file_names_list(self):
        file_names_list = []
        for f in self.my_files:
            file_names_list.append(f.getFileName())   # only need the name, not the whole pyFile object
        return file_names_list

    def get_added_lines_in_commit(self):
        return self.__added_lines_in_commit

    def get_deleted_lines_in_commit(self):
        return self.__deleted_lines_in_commit

    def get_added_test_loc(self):
        return self.__added_test_loc

    def get_deleted_test_loc(self):
        return self.__deleted_test_loc

    def get_number_of_transformations(self):
        return self.number_of_transformations

    def get_nbr_test_files(self):
        return self.__nbr_test_files

    def get_nbr_prod_files(self):
        return self.__nbr_prod_files

    def get_transformations(self):
        return self.transformations

    def set_commit_nbr(self, value):
        self.__commit_nbr = value

    def set_commit_type(self, value):
        self.__commitType = value

    def set_added_lines_in_commit(self, value):
        self.__added_lines_in_commit = value

    def add_added_lines_in_commit(self, value):
        self.__added_lines_in_commit = self.__added_lines_in_commit + value

    def set_deleted_lines_in_commit(self, value):
        self.__deleted_lines_in_commit = value

    def add_deleted_lines_in_commit(self, value):
        self.__deleted_lines_in_commit = self.__deleted_lines_in_commit + value

    def set_added_test_loc(self, value):
        self.__added_test_loc = value

    def add_added_test_loc(self, value):
        self.__added_test_loc = self.__added_test_loc + value

    def set_deleted_test_loc(self, value):
        self.__deleted_test_loc = value

    def add_deleted_test_loc(self, value):
        self.__deleted_test_loc = self.__deleted_test_loc + value

    def set_number_of_transformations(self, value):
        self.__number_of_transformations = value

    def add_number_of_transformations(self, value):
        self.number_of_transformations = self.number_of_transformations + value

    def set_nbr_test_files(self, value):
        self.__nbr_test_files = value

    def increment_nbr_test_files(self):
        self.__nbr_test_files += 1

    def set_nbr_prod_files(self, value):
        self.__nbr_prod_files = value

    def increment_nbr_prod_files(self):
        self.__nbr_prod_files += 1

    def set_transformations(self, value):
        self.transformations.append(value)

    def del_commit_nbr(self):
        del self.__commit_nbr

    def del_commit_type(self):
        del self.__commitType

    def del_added_lines_in_commit(self):
        del self.__added_lines_in_commit

    def del_deleted_lines_in_commit(self):
        del self.__deleted_lines_in_commit

    def del_added_test_loc(self):
        del self.__added_test_loc

    def del_deleted_test_loc(self):
        del self.__deleted_test_loc

    def del_number_of_transformations(self):
        del self.__number_of_transformations

    def del_nbr_test_files(self):
        del self.__nbr_test_files

    def del_nbr_prod_files(self):
        del self.__nbr_prod_files

    # def del_transformations(self):
    #    del self.__transformations

    commit_nbr = property(get_commit_nbr, set_commit_nbr, del_commit_nbr, "commit_nbr's docstring")
    # commitType = property(get_commit_type, set_commit_type, del_commit_type, "commitType's docstring")
    added_lines_in_commit = property(get_added_lines_in_commit, set_added_lines_in_commit, del_added_lines_in_commit, "added_lines_in_commit's docstring")
    deleted_lines_in_commit = property(get_deleted_lines_in_commit, set_deleted_lines_in_commit, del_deleted_lines_in_commit, "deleted_lines_in_commit's docstring")
    added_test_loc = property(get_added_test_loc, set_added_test_loc, del_added_test_loc, "added_test_loc's docstring")
    deleted_test_loc = property(get_deleted_test_loc, set_deleted_test_loc, del_deleted_test_loc, "deleted_test_loc's docstring")
    nbr_test_files = property(get_nbr_test_files, set_nbr_test_files, del_nbr_test_files, "nbr_test_files's docstring")
    nbr_prod_files = property(get_nbr_prod_files, set_nbr_prod_files, del_nbr_prod_files, "nbr_prod_files's docstring")
    added_ta_test_loc = property(get_added_tatest_loc, set_added_tatest_loc, del_added_tatest_loc, "added_ta_test_loc's docstring")

if __name__ == "__main__":
    Commit.load_recommendations()
