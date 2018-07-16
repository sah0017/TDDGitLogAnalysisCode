"""
Created on Jul 25, 2014

@author: susan hammond

Used by:  runGitFileAnalysis
Uses:  GitFile
Parameters:  a path to a student's submission and the git file to be analyzed
Results:  analyzes a git file and stores the data in a .json file
"""
import GitFile
import os


class SubmissionReport:

    __totalSubmissions = 0
    __totalCommitsInAnalysis = 0
    __totalTransformationsInAnalysis = 0
    __totalAntiTransformationsInAnalysis = 0
    __totalLinesOfCodeInAnalysis = 0

    def __init__(self):
        pass

    def analyze_git_log(self, path, file_name, which_assignment):
        self.add_to_total_submissions_in_analysis(1)
        my_git_file = GitFile.GitFile()                       # instantiates a git log file object

        my_git_file.analyzeGitLogFile(path + os.sep + file_name)        # reads through entire git log file and performs TDD/TPP analyzes
        file_parts = os.path.splitext(file_name)
        my_git_file.GenerateInvididualReport(path, file_parts[0], which_assignment)
                
        my_git_file.storeGitReportObject(path + os.sep + file_parts[0])

    @classmethod
    def get_total_commits(cls):
        return cls.__totalCommitsInAnalysis

    @classmethod
    def get_total_transformations(cls):
        return cls.__totalTransformationsInAnalysis

    @classmethod
    def get_total_anti_transformations(cls):
        return cls.__totalAntiTransformationsInAnalysis

    @classmethod
    def get_total_lines_of_code(cls):
        return cls.__totalLinesOfCodeInAnalysis

    @classmethod
    def get_total_submissions(cls):
        return cls.__totalSubmissions

    @classmethod
    def set_total_commits(cls, value):
        cls.__totalCommitsInAnalysis = value

    @classmethod
    def add_to_total_commits_in_analysis(cls, value):
        cls.__totalCommitsInAnalysis = cls.__totalCommitsInAnalysis + value

    @classmethod
    def set_total_transformations(cls, value):
        cls.__totalTransformationsInAnalysis = value

    @classmethod
    def set_total_anti_transformations(cls, value):
        cls.__totalAntiTransformationsInAnalysis = value

    @classmethod
    def set_total_lines_of_code(cls, value):
        cls.__totalLinesOfCodeInAnalysis = value

    @classmethod
    def set_total_submissions(cls, value):
        cls.__totalSubmissions = value

    @classmethod
    def add_to_total_submissions_in_analysis(cls, value):
        cls.__totalSubmissions = cls.__totalSubmissions + value

    @classmethod
    def set_trans_totals_by_tran_type(cls, value):
        cls.__transTotalsInAnalysis = value

    @classmethod
    def set_antitrans_totals_by_tran_type(cls, value):
        cls.__antitransTotalsInAnalysis = value

    @classmethod
    def del_total_commits(cls):
        del cls.__totalCommitsInAnalysis

    @classmethod
    def del_total_transformations(cls):
        del cls.__totalTransformationsInAnalysis

    @classmethod
    def del_total_anti_transformations(cls):
        del cls.__totalAntiTransformationsInAnalysis

    @classmethod
    def del_total_lines_of_code(cls):
        del cls.__totalLinesOfCodeInAnalysis

    @classmethod
    def del_total_submissions(cls):
        del cls.__totalSubmissions
