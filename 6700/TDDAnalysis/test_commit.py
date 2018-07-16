import unittest
import sys
sys.path.append("../")
import Commit
import FileHandler

class MyCommitGradeTestCase(unittest.TestCase):
    """
    current configuration values
    RedLightWithProdCode:  "1, 10"
    GreenLightWithTestCode:  "1, 10"
    OneTransformation:  "1, 5"
    LargeCommits:  "10, 5"
    """

    def test_red_light_contains_prod_files(self):
        my_file_io = FileHandler.FileHandler()
        my_file_io.open_file("RedLightCommitTest.txt")
        myCommit = Commit.Commit(1, my_file_io)
        Commit.Commit.load_grade_criteria()
        myCommit.set_added_lines_in_commit(0)
        myCommit.set_added_test_loc(10)
        myCommit.add_number_of_transformations(1)
        myCommit.set_nbr_test_files(1)
        myCommit.set_nbr_prod_files(2)
        self.assertEqual(myCommit.calculate_tdd_grade(), 96)

    def test_green_light_contains_test_files(self):
        my_file_io = FileHandler.FileHandler()
        my_file_io.open_file("GreenLightCommitTest.txt")
        myCommit = Commit.Commit(1, my_file_io)
        Commit.Commit.load_grade_criteria()
        myCommit.set_added_lines_in_commit(0)
        myCommit.set_added_test_loc(10)
        myCommit.add_number_of_transformations(1)
        myCommit.set_nbr_test_files(2)
        myCommit.set_nbr_prod_files(1)
        self.assertEqual(myCommit.calculate_tdd_grade(), 96)

    def test_largecommit(self):
        my_file_io = FileHandler.FileHandler()
        my_file_io.open_file("GreenLightCommitTest.txt")
        myCommit = Commit.Commit(1, my_file_io)
        Commit.Commit.load_grade_criteria()
        myCommit.set_added_lines_in_commit(20)
        myCommit.set_added_test_loc(10)
        myCommit.add_number_of_transformations(1)
        myCommit.set_nbr_test_files(1)
        myCommit.set_nbr_prod_files(1)
        self.assertEqual(myCommit.calculate_tdd_grade(), 96)

    def test_onetransformation(self):
        my_file_io = FileHandler.FileHandler()
        my_file_io.open_file("GreenLightCommitTest.txt")
        myCommit = Commit.Commit(1, my_file_io)
        Commit.Commit.load_grade_criteria()
        myCommit.set_added_lines_in_commit(0)
        myCommit.set_added_test_loc(10)
        myCommit.add_number_of_transformations(2)
        myCommit.set_nbr_test_files(1)
        myCommit.set_nbr_prod_files(1)
        self.assertEqual(myCommit.calculate_tdd_grade(), 98)

if __name__ == '__main__':
    unittest.main()
