"""
Created on June 6, 2017

@author: susan hammond
"""
import ConfigParser

import GitFile
import Assignment
import os
import CodeCoverage


class ProcessConformance(object):
    """
    The ProcessConformance object will collect the various pieces of data we will use to try and
    determine TDD and TPP process conformance.  Will result in data to be used in a radar chart.
    """

    def __init__(self):
        Assignment.Assignment.loadAssignments()
        self.assignmentList = Assignment.Assignment.get_assignment_list()
        self.myCodeCov = CodeCoverage.CodeCoverage()
        self.myCodeCov.loadCoverageReports(reportRoot, self.assignmentList)  # load up available code coverage reports; they're small, text-based files
        self.invalidRedLights = 0
        self.invalidGreenLights = 0
        master_file = open(reportRoot + os.sep + "Overall Process Conformance Report.csv", "w")
        master_file.write("Student Name\n  Assignment Name, Total Commits, Red Light Validity Ratio, "
                       "Green Light Validity Ratio, "
                       "TPP Conformance Ratio, "
                       "Nbr TDD Cycles, Nbr Valid TDD Cycles, Nbr Ideal Cycles, Code Coverage")
        master_file.close()

    def create_process_conformance_report(self, report_root, analysis_root, file_name, student_name):
        my_git_file = GitFile.GitFile()
        current_git_file = my_git_file.retrieveGitReportObject(analysis_root + os.sep + file_name)
        if current_git_file is not None:
            out_file = open(report_root + os.sep + student_name + " Process Conformance Report" + ".csv", "w")
            out_file.write("Assignment Name, Total Commits, Red Light Validity Ratio, "
                               "Green Light Validity Ratio, "
                               "TPP Conformance Ratio, "
                               "Nbr TDD Cycles, Nbr Valid TDD Cycles, Nbr Ideal Cycles, Code Coverage")
            self.collect_process_conformance_data(current_git_file, out_file, report_root, student_name)
            out_file.close()

    def collect_process_conformance_data(self, git_file, out_file, report_root, student_name):
        assignments_list = git_file.getAssignments()
        with open(os.path.join(report_root + os.sep + "Overall Process Conformance Report.csv"), "a+") as masterFile:
            masterFile.write("\n\n" + student_name + "\n")
        for assignment in assignments_list:
            try:
                commits = assignment.get_my_commits()
            except:
                commits = None
            tdd_cycles = assignment.get_my_tddcycles()
            if tdd_cycles is None:
                nbr_t_d_d_cycles = 0
            else:
                nbr_t_d_d_cycles = len(tdd_cycles)
            ideal_cycles = 0
            commit_stats = assignment.get_my_commit_totals()
            for cstats in commit_stats:
                ideal_cycles += cstats.get_ideal_number_of_cycles()
            total_r_l = 0
            invalid_r_l = 0
            invalid_g_l = 0
            total_g_l = 0
            commits_with_too_many_trans = 0
            if commits is not None:
                for myCommit in commits:
                    if myCommit.get_number_of_transformations() > 1:
                        commits_with_too_many_trans += 1
                    commit_validity = myCommit.get_commit_validity()
                    commit_type = myCommit.get_commit_type()
                    if commit_type == "Red Light":
                        total_r_l += 1
                        if commit_validity == "INVALID":
                            invalid_r_l += 1
                    elif commit_type == "Green Light":
                        total_g_l += 1
                        if commit_validity == "INVALID":
                            invalid_g_l += 1
            self.invalidRedLights = invalid_r_l
            self.invalidGreenLights = invalid_g_l
            valid_cycles = 0
            for my_t_d_d_cycle in tdd_cycles:
                if my_t_d_d_cycle is not None:
                    if my_t_d_d_cycle.is_cycle_valid():
                        valid_cycles += 1
            nbr_of_commits = len(commits)
            if total_r_l == 0:
                invalid_r_l_ratio = 0.0
            else:
                invalid_r_l_ratio = (total_r_l - self.invalidRedLights) / float(total_r_l)
            if total_g_l == 0:
                invalid_g_l_ratio = 0.0
            else:
                invalid_g_l_ratio = (total_g_l - self.invalidGreenLights) / float(total_g_l)
            if nbr_of_commits == 0:
                t_p_p_conformance_ratio = 0.0
            else:
                t_p_p_conformance_ratio = (nbr_of_commits - commits_with_too_many_trans) / float(nbr_of_commits)
            student_name = student_name.replace(" ", "")
            cc_pct = self.myCodeCov.retrieveCodeCoverageForSpecificStudentAndAssignment(student_name, assignment.assignmentName)
            if isinstance(cc_pct, float):
                cc_pct = format(cc_pct, '.2f')

            with open(os.path.join(report_root + os.sep + "Overall Process Conformance Report.csv"), "a+") as masterFile:
                masterFile.write("\r" + assignment.assignmentName + ", " +
                            str(nbr_of_commits) + ", " +
                            format(invalid_r_l_ratio, '.2f') + ", " +
                            format(invalid_g_l_ratio, '.2f') + ", " +
                            format(t_p_p_conformance_ratio, '.2f') + ", " +
                            str(nbr_t_d_d_cycles) + ", " +
                            str(valid_cycles) + ", " +
                            str(ideal_cycles) + ", " +
                            str(cc_pct))

            out_file.write("\r" + assignment.assignmentName + ", " +
                           str(nbr_of_commits) + ", " +
                           format(invalid_r_l_ratio, '.2f') + ", " +
                           format(invalid_g_l_ratio, '.2f') + ", " +
                           format(t_p_p_conformance_ratio, '.2f') + ", " +
                           str(nbr_t_d_d_cycles) + ", " +
                           str(valid_cycles) + ", " +
                           str(ideal_cycles) + ", " +
                           str(cc_pct))


if __name__ == '__main__':
    myConfig = ConfigParser.ConfigParser()
    myConfig.read("TDDanalysis.cfg")
    myDrive = myConfig.get("Location","Root")
    myHome = myConfig.get("Location","Home")
    printToFile = True
    mySemester = myConfig.get("Location","Semester")
    myAssignment = myConfig.get("Location","Assignment")
    analysisRoot = os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + myAssignment)
    reportRoot = os.path.join(myDrive + os.sep + myHome + os.sep + mySemester)
    myReport = ProcessConformance()

    for gitDataFile in os.listdir(analysisRoot):
        if os.path.isfile(os.path.join(analysisRoot, gitDataFile)):
            fileName, ext = os.path.splitext(gitDataFile)
            if ext == ".json":
                studentName = fileName.split("_")
                print 'Processing ' + studentName[0]
                myReport.create_process_conformance_report(reportRoot,
                                                           analysisRoot,
                                                           fileName, studentName[0])
