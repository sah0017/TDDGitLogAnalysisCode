"""
Created on Apr 12, 2016

@author: susan hammond
"""
import os
import GitFile
import Transformations
import AssignmentTotals
import Assignment


class AnalysisReport(object):

    def __init__(self):
        self.out_file = None
        self.assignment_list = Assignment.Assignment.get_assignment_list()

    def create_analysis_report(self, report_root, analysis_root, my_assignment, which_assignment, prod_path):
        my_dir = os.listdir(analysis_root)

        self.out_file = open(report_root + os.sep + "Report" + my_assignment + ".csv", "w")
        my_trans_names = Transformations.Trans()
        self.out_file.write("Submission name, Assignment Name, TDD Score, Nbr Ideal Cycles, Nbr TDD Cycles, "                           
                            "Nbr Valid TDD Cycles, Nbr of Commits, Nbr Non Empty Commits, "
                            "Red Light, Invalid RL, "
                            "Nbr Consec RL, Reasons-Undetermined, Same test file, "
                            "Same prod file, Multiple files, "
                            "Green Light, Invalid GL, Nbr Consec GL, Reasons-Undetermined, "
                            "Same test file, Same prod file, "
                            "Multiple files, Refactor, Other, Commits w/Prod Code, Avg Lines Per All Commits, "  
                            "Nbr of Trans, Avg Trans Per Prod Commit,Avg Prod LOC per Trans per Prod Commit, "
                            "Ratio-Prod to Test Code, Net Added Prod Lines, Net Added Test Lines, % of commits RL, % of commits GL\r")

        indiv_assignment_totals = self.print_individual_totals_and_count_assignment_totals(my_dir, analysis_root,
                                                                                           which_assignment,
                                                                                           my_assignment, prod_path)

        ttl_sub = AssignmentTotals.AssignmentTotals.get_total_submissions()
        ttl_comm = AssignmentTotals.AssignmentTotals.get_total_commits()
        ttl_non_empty_comm = AssignmentTotals.AssignmentTotals.get_total_non_empty_commits()
        ttl_trans = AssignmentTotals.AssignmentTotals.get_total_nbr_transformations()
        trans_ttls_list = AssignmentTotals.AssignmentTotals.get_total_trans_by_type()
        # ttlAntiTrans = myAssignmentStats.get_total_anti_transformations()
        anti_trans_ttls_list = AssignmentTotals.AssignmentTotals.get_total_antitrans_by_type()
        ttl_l_o_c = AssignmentTotals.AssignmentTotals.get_total_prod_LOC()
        ttl_loc_test = AssignmentTotals.AssignmentTotals.get_total_test_LOC()
        self.out_file.write("\n\r\n\rAssignment report" + " \n\r")
        self.out_file.write("Assignment:  ,Totals,")
        if which_assignment == "all":
            for name in self.assignment_list:
                self.out_file.write(str(name) + ",")
            self.out_file.write("\n\r")
        self.out_file.write("Total submissions analyzed:  ," + str(ttl_sub))
        if which_assignment == "all":
            for name in self.assignment_list:
                self.out_file.write("," + str(indiv_assignment_totals[name].get_nbr_submissions()))
        self.out_file.write("\n\r")
        self.out_file.write("Total nbr of commits:  ," + str(ttl_comm))
        if which_assignment == "all":
            for name in self.assignment_list:
                self.out_file.write("," + str(indiv_assignment_totals[name].get_nbr_commits()))
        self.out_file.write("\r")
        self.out_file.write("Total nbr of non-empty commits:  ," + str(ttl_non_empty_comm))
        if which_assignment == "all":
            for name in self.assignment_list:
                self.out_file.write("," + str(indiv_assignment_totals[name].get_nbr_non_empty_commits()))
        self.out_file.write("\r")
        self.out_file.write("Total nbr of transformations:  ," + str(ttl_trans))
        if which_assignment == "all":
            for name in self.assignment_list:
                self.out_file.write("," + str(indiv_assignment_totals[name].get_total_nbr_transformations_in_assignment()))
        self.out_file.write("\r")
        for i in range(0, 13):
            self.out_file.write("Nbr of trans type " + my_trans_names.getTransformationName(i) +
                                " is ," + str(trans_ttls_list[i]))
            if which_assignment == "all":
                for name in self.assignment_list:
                    trans_list = indiv_assignment_totals[name].get_total_trans_by_type_in_assignment()
                    self.out_file.write(", " + str(trans_list[i]))
            self.out_file.write("\r")
        # out_file.write( "Total number of anti-transformations:  ," + str(ttlAntiTrans)+" \r")
        self.out_file.write("\n\r")
        for i in range(1, 9):
            if anti_trans_ttls_list[i] != 0:
                self.out_file.write("Nbr of anti-trans type " +
                                    my_trans_names.getTransformationName(-i) + " is ," +
                                    str(anti_trans_ttls_list[i]) + "\r")

        self.out_file.write("\n\r Total prod lines of code:  ," + str(ttl_l_o_c))
        if which_assignment == "all":
            for name in self.assignment_list:
                self.out_file.write("," + str(indiv_assignment_totals[name].get_net_prod_loc_added()))
        self.out_file.write("\r")
        self.out_file.write("\r Total test lines of code:  ," + str(ttl_loc_test))
        if which_assignment == "all":
            for name in self.assignment_list:
                self.out_file.write("," + str(indiv_assignment_totals[name].get_net_test_loc_added()))
        self.out_file.write("\r")
        if ttl_non_empty_comm > 0:
            self.out_file.write("Avg Trans per commit: , " + format(AssignmentTotals.AssignmentTotals.get_total_avg_trans_per_commit(), '.2f'))
            if which_assignment == "all":
                for name in self.assignment_list:
                    self.out_file.write("," + format(indiv_assignment_totals[name].get_avg_trans_per_commit(), '.2f'))
            self.out_file.write("\r")
            self.out_file.write("Avg loc per commit:  ," + format(AssignmentTotals.AssignmentTotals.get_total_avg_lines_per_commit(), '.2f'))
            if which_assignment == "all":
                for name in self.assignment_list:
                    self.out_file.write("," + format(indiv_assignment_totals[name].get_avg_lines_per_commit(), '.2f'))
            self.out_file.write("\r")
        self.out_file.close()
    
    def print_individual_totals_and_count_assignment_totals(self, my_dir, analysis_root, which_assignment,
                                                            my_assignment_name, prod_path):
        my_git_file = GitFile.GitFile()
        my_totals = {}
        if which_assignment == "all":
            for key in self.assignment_list:
                my_totals[key] = AssignmentTotals.AssignmentTotals()
        else:
            my_totals[my_assignment_name] = AssignmentTotals.AssignmentTotals()
        for item in my_dir:
            if os.path.isfile(os.path.join(analysis_root, item)):
                file_name, ext = os.path.splitext(item)
                if ext == ".gitdata":
                    student_name = file_name.split("_")
                    print 'Processing ' + student_name[0]
                    current_git_file = my_git_file.retrieveGitReportObject(analysis_root + os.sep + file_name)
                    if current_git_file is not None:
                        total_tests = self.count_total_tests(analysis_root, file_name, prod_path)

                        AssignmentTotals.AssignmentTotals.add_to_total_submissions(1)
                        student_submission_totals = AssignmentTotals.AssignmentTotals()
        
                        my_assignments = current_git_file.getAssignments()
                        my_assignment_total_commits_with_prod_code = 0

                        for my_assignment in my_assignments:
                            assignment_name = my_assignment.get_assignment_name().lower()
                            if assignment_name == my_assignment_name or which_assignment == "all":
                                my_totals[assignment_name].add_to_nbr_submissions(1)
                                my_commit_stats_list = my_assignment.get_my_commit_totals()
                                my_commit_list = my_assignment.get_my_commits()

                                '''
                                myTransformationsByTranType = my_assignment.get_trans_totals_by_tran_type()
                                myAntiTransformationsByTranType = my_assignment.get_antitrans_totals_by_tran_type() 
                                '''
                                for my_commit_stats in my_commit_stats_list:
                                    nbr_commits = my_commit_stats.get_nbr_commits()
                                    nbr_non_empty_commits = my_commit_stats.get_nbr_non_empty_commits()
                                    student_submission_totals.set_nbr_commits(nbr_commits)
                                    student_submission_totals.set_nbr_non_empty_commits(nbr_non_empty_commits)
                                    my_totals[assignment_name].set_nbr_commits(nbr_commits)
                                    my_totals[assignment_name].set_nbr_non_empty_commits(nbr_non_empty_commits)
                                    AssignmentTotals.AssignmentTotals.set_total_commits(nbr_commits)
                                    AssignmentTotals.AssignmentTotals.set_total_non_empty_commits(nbr_non_empty_commits)

                                    student_submission_totals.set_rlcommit(my_commit_stats.get_rlcommit())
                                    student_submission_totals.set_glcommit(my_commit_stats.get_glcommit())
                                    student_submission_totals.set_other_commit(my_commit_stats.get_other_commit())
                                    student_submission_totals.set_ref_commit(my_commit_stats.get_ref_commit())

                                    added_loc = my_commit_stats.get_added_lines_in_assignment()
                                    student_submission_totals.set_added_lines_in_assignment(added_loc)
                                    my_totals[assignment_name].set_added_lines_in_assignment(added_loc)
                                    AssignmentTotals.AssignmentTotals.set_total_prod_LOC(added_loc)
                                    added_test_loc = my_commit_stats.get_added_test_locin_assignment()
                                    student_submission_totals.set_added_test_locin_assignment(added_test_loc)
                                    my_totals[assignment_name].set_added_test_locin_assignment(added_test_loc)
                                    AssignmentTotals.AssignmentTotals.set_total_test_LOC(added_test_loc)
                                    del_prod = my_commit_stats.get_deleted_lines_in_assignment()
                                    student_submission_totals.set_deleted_lines_in_assignment(del_prod)
                                    my_totals[assignment_name].set_deleted_lines_in_assignment(del_prod)
                                    AssignmentTotals.AssignmentTotals.set_total_deleted_prod_lines(del_prod)
                                    del_test = my_commit_stats.get_deleted_test_locin_assignment()
                                    AssignmentTotals.AssignmentTotals.set_total_deleted_test_lines(del_test)
                                    student_submission_totals.set_deleted_test_locin_assignment(del_test)
                                    my_totals[assignment_name].set_deleted_test_locin_assignment(del_test)

                                    student_submission_totals.set_total_trans_by_type_in_assignment(my_commit_stats.get_total_trans_by_type_in_assignment())
                                    student_submission_totals.set_total_anti_trans_by_type_in_assignment(my_commit_stats.get_total_anti_trans_by_type_in_assignment())

                                    net_prod_lines_added = my_commit_stats.addedLinesInAssignment - my_commit_stats.deletedLinesInAssignment
                                    net_test_lines_added = my_commit_stats.addedTestLOCInAssignment - my_commit_stats.deletedTestLOCInAssignment
                                    if my_assignment.nbr_commits_with_prod_code > 0:
                                        my_assignment_total_commits_with_prod_code += my_assignment.nbr_commits_with_prod_code
                                        avg_trans_commit = (my_commit_stats.get_total_nbr_transformations_in_assignment() + \
                                                       my_commit_stats.get_total_nbr_anti_transformations_in_assignment()) / float(my_assignment.nbr_commits_with_prod_code)
                                        avg_loc_trans_commit = float(net_prod_lines_added) / (
                                                    my_commit_stats.get_total_nbr_transformations_in_assignment() + \
                                                    my_commit_stats.get_total_nbr_anti_transformations_in_assignment()) / float(
                                            my_assignment.nbr_commits_with_prod_code)
                                    else:
                                        avg_trans_commit = 0
                                        avg_loc_trans_commit = 0

                                    self.out_file.write(file_name + ext + "," + str(my_assignment.assignmentName) + "," +
                                                        str(my_assignment.tdd_grade) + "," +

                                                        str(my_commit_stats.get_ideal_number_of_cycles()) + "," +
                                                        str(my_assignment.getTDDCycleCount()) + "," +
                                                        str(my_assignment.get_nbr_valid_cycles()) + ", " +
                                                        str(my_commit_stats.nbrCommits) + "," +
                                                        str(my_commit_stats.nbrNonEmptyCommits) + "," +
                                                        str(my_commit_stats.RLCommit) + "," +
                                                        str(my_commit_stats.get_invalid_rl_commits()) + "," +
                                                        str(my_assignment.getConsecutiveRedLights()) +
                                                        my_assignment.getReasonsForConsecutiveCommits("Red Light") + "," +
                                                        str(my_commit_stats.GLCommit) + "," +
                                                        str(my_commit_stats.get_invalid_gl_commits()) + "," +
                                                        str(my_assignment.getConsecutiveGreenLights()) +
                                                        my_assignment.getReasonsForConsecutiveCommits("Green Light") + "," +
                                                        str(my_commit_stats.refCommit) + "," +
                                                        str(my_commit_stats.otherCommit) + "," +
                                                        str(my_assignment.nbr_commits_with_prod_code) + "," +
                                                        format(my_commit_stats.get_avg_lines_per_commit(), '.2f') + "," +
                                                        str(my_commit_stats.get_total_nbr_transformations_in_assignment() +
                                                        my_commit_stats.get_total_nbr_anti_transformations_in_assignment()) + "," +
                                                        format(avg_trans_commit, '.2f') + " ," +
                                                        format(avg_loc_trans_commit, '.2f') + " ," +
                                                        format(my_commit_stats.get_ratio_prod_to_test(), '.2f') + "," +
                                                        str(net_prod_lines_added) + "," +
                                                        str(net_test_lines_added) + "," +
                                                        format(self.calc_percentage(my_assignment.assignmentName, my_commit_stats.RLCommit, my_commit_stats.nbrCommits), '.1f') +
                                                        "," + format(self.calc_percentage(my_assignment.assignmentName, my_commit_stats.GLCommit,
                                                            my_commit_stats.nbrCommits), '.2f') + "\r")

                                for my_commit in my_commit_list:
                                    AssignmentTotals.AssignmentTotals.set_total_nbr_transformations(my_commit.get_number_of_transformations())
                                    AssignmentTotals.AssignmentTotals.set_total_prod_files(my_commit.get_nbr_prod_files())
                                    AssignmentTotals.AssignmentTotals.set_total_test_files(my_commit.get_nbr_test_files())
                                    my_files = my_commit.get_file_list()
                                    for my_file in my_files:
                                        my_trans = my_file.get_transformations()
                                        for my_tran in my_trans:
                                            if my_tran >= 0:
                                                AssignmentTotals.AssignmentTotals.set_total_trans_by_type(1, my_tran)
                                                my_totals[assignment_name].add_total_trans_by_type_in_assignment(1, my_tran)

                                            else:
                                                AssignmentTotals.AssignmentTotals.set_total_antitrans_by_type(1, abs(my_tran))
                                                my_totals[assignment_name].add_total_anti_trans_by_type_in_assignment(1, abs(my_tran))
                        if my_assignment_total_commits_with_prod_code > 0:
                            tot_avg_trans_commit = (student_submission_totals.get_total_nbr_transformations_in_assignment() + \
                                               student_submission_totals.get_total_nbr_anti_transformations_in_assignment()) / float(
                                    my_assignment_total_commits_with_prod_code)
                            tot_avg_loc_trans_commit = float(net_prod_lines_added) / \
                                    (student_submission_totals.get_total_nbr_transformations_in_assignment() + \
                                    student_submission_totals.get_total_nbr_anti_transformations_in_assignment()) / float(
                                    my_assignment_total_commits_with_prod_code)
                        else:
                            tot_avg_trans_commit = 0
                            tot_avg_loc_trans_commit = 0
                        self.out_file.write("Totals for " + student_name[0] + "," + str(len(my_assignments)) +
                                        ",Total Student Tests, " + str(total_tests) + "," +
                                        ",," +
                                        str(student_submission_totals.nbrCommits) + "," +
                                        str(student_submission_totals.get_total_non_empty_commits()) + "," +
                                        str(student_submission_totals.RLCommit) + ",,,,,,," +
                                        str(student_submission_totals.GLCommit) + ",,,,,,," +
                                        str(student_submission_totals.refCommit) + "," +
                                        str(student_submission_totals.otherCommit) + ",," +
                                        format(student_submission_totals.get_avg_lines_per_commit(), '.2f') + ",," +
                                        format(tot_avg_trans_commit, '.2f') + "," +
                                        format(tot_avg_loc_trans_commit, '.2f') + " ," +
                                        format(student_submission_totals.get_ratio_prod_to_test(), '.2f') + "," +
                                        str(student_submission_totals.get_net_prod_loc_added()) + "," +
                                        str(student_submission_totals.get_net_test_loc_added()) + "," + "\r\r")
        return my_totals

    def count_total_tests(self, path, student, prod_path):
        nbr_tests = 0

        file_path = os.path.join(path, "submissions", student, prod_path, "test")
        if not os.path.isdir(file_path):
            file_path = os.path.join(path, "submissions", student, "test")
            if not os.path.isdir(file_path):
                file_path = os.path.join(path, "submissions", student)
        files = os.listdir(file_path)
        for pyfile in files:
            file_name, ext = os.path.splitext(pyfile)
            if ext == ".py" and "test" in file_name.lower():
                with open(os.path.join(file_path, pyfile)) as test_file:
                    for line in test_file:
                        clean_line = line.strip()
                        if clean_line.startswith("def") and "test" in line.lower():
                            nbr_tests += 1
        return nbr_tests

    def calc_percentage(self, which_type, nbr_type_commits, nbr_commits):
        if which_type != self.assignment_list[0]:
            return nbr_type_commits / float(nbr_commits)
        else:
            return ""



if __name__ == '__main__':
    myReport = AnalysisReport()
    myReport.create_analysis_report("/Users/shammond/GoogleDrive/6700Fall18",
                                    "/Users/shammond/GoogleDrive/6700Fall18/rcube", "rcube2", "rcube2", "RCube")
