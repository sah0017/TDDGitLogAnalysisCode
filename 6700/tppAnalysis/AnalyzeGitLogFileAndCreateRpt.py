'''
Created on Jul 25, 2014

@author: susanha

Used by:  runGitFileAnalysis
Uses:  GitFile
Parameters:  a path to a student's submission and the git file to be analyzed
Results:  analyzes a git file and stores the data in a .json file
'''
import GitFile
import os
import Transformations
import AssignmentTotals


class SubmissionReport:

    __totalSubmissions = 0
    __totalCommitsInAnalysis = 0
    __totalTransformationsInAnalysis = 0
    __totalAntiTransformationsInAnalysis = 0
    __totalLinesOfCodeInAnalysis = 0

    def __init__(self):
        pass

    def analyzeGitLog(self, path, fileName):
        self.add_to_total_submissions_in_analysis(1)
        myGitFile = GitFile.GitFile()                       # instantiates a git log file object

        myGitFile.analyzeGitLogFile(path+os.sep+fileName)        # reads through entire git log file and performs TDD/TPP analyzes
        fileParts = os.path.splitext((fileName))
        myAssignments = myGitFile.GenerateInvididualReport(path, fileParts[0])
                
        #myGitFile.setAssignments(myAssignments)    # Add commit stats to git file object
        myGitFile.storeGitReportObject(path+os.sep+fileParts[0])
    
    

        #return myAssignments

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

    def get_trans_totals_by_tran_type(cls):
        return cls.__transTotalsInAnalysis

    @classmethod

    def get_antitrans_totals_by_tran_type(cls):
        return cls.__antitransTotalsInAnalysis

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

    @classmethod

    def del_trans_totals(cls):
        del cls.__transTotalsInAnalysis

    @classmethod

    def del_antitrans_totals(cls):
        del cls.__antitransTotalsInAnalysis
    '''    
    __totalCommitsInAnalysis = property(get_total_commits, set_total_commits, del_total_commits, "totalCommits's docstring")
    __totalTransformationsInAnalysis = property(get_total_transformations, set_total_transformations, del_total_transformations, "totalTransformations's docstring")
    __totalAntiTransformationsInAnalysis = property(get_total_anti_transformations, set_total_anti_transformations, del_total_anti_transformations, "totalAntiTransformations's docstring")
    __totalLinesOfCodeInAnalysis = property(get_total_lines_of_code, set_total_lines_of_code, del_total_lines_of_code, "totalLinesOfCode's docstring")
    #__totalSubmissions = property(get_total_submissions, set_total_submissions, del_total_submissions, "totalSubmissions's docstring")
    __transTotalsInAnalysis = property(get_trans_totals_by_tran_type, set_trans_totals_by_tran_type, del_trans_totals, "transTotals's docstring")
    __antitransTotalsInAnalysis = property(get_antitrans_totals_by_tran_type, set_antitrans_totals_by_tran_type, del_antitrans_totals, "antitransTotals's docstring")
    '''
