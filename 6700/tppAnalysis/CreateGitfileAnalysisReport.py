'''
Created on Apr 12, 2016

@author: susanha
'''
import os
import GitFile
import Transformations
import AnalyzeGitLogFileAndCreateRpt
import AssignmentTotals


class AnalysisReport(object):
    pass

    def createAnalysisReport(self, reportRoot, analysisRoot, pToF, myAssignment):
        printToFile = pToF
        myDir = os.listdir(analysisRoot)
        myAssignmentTotals = []
        
        self.outFile = open(reportRoot + os.sep + "Report" + myAssignment + ".csv", "w")
        myTransNames = Transformations.Trans()
        self.outFile.write("Submission name, Assignment Name, Nbr Ideal Cycles, Nbr TDD Cycles, "
                           "Nbr Valid TDD Cycles, Nbr of Commits, "
                           "Red Light, Invalid RL, "
                           "Nbr Consec RL, Reasons-Undetermined, Same test file, "
                           "Same prod file, Multiple files, "
                           "Green Light, Invalid GL, Nbr Consec GL, Reasons-Undetermined, "
                           "Same test file, Same prod file, "
                           "Multiple files, Refactor, Other, Avg Lines Per Commit, Avg Trans Per Commit,"
                           "Ratio-Prod to Test Code, Added Prod Lines, Added Test Lines, Del/Mod Lines,"
                           "Del/Mod Test Lines\r")

        self.printIndividualTotalsAndCountAssignmentTotals(myDir, analysisRoot, printToFile, myTransNames)
        
        assignment = 1
        #for myAssignmentStats in myTotals:
            
        ttlSub = AssignmentTotals.AssignmentTotals.get_total_submissions()
        ttlComm = AssignmentTotals.AssignmentTotals.get_total_commits()
        ttlTrans = AssignmentTotals.AssignmentTotals.get_total_nbr_transformations()
        transTtlsList = AssignmentTotals.AssignmentTotals.get_total_trans_by_type()
        #ttlAntiTrans = myAssignmentStats.get_total_anti_transformations()
        antiTransTtlsList = AssignmentTotals.AssignmentTotals.get_total_antitrans_by_type()
        ttlLOC = AssignmentTotals.AssignmentTotals.get_total_LOC()
        if printToFile:
            self.outFile.write( "\n\r\n\rAssignment report"+" \n\r")
            self.outFile.write("Assignment:  ," + str(assignment)+"\n\r")
            self.outFile.write( "Total submissions analyzed:  ," + str(ttlSub)+" \n\r")
            self.outFile.write( "Total nbr of commits:  ," + str(ttlComm)+" \r")
            self.outFile.write( "Total nbr of transformations:  ," + str(ttlTrans)+" \r")
            for i in range(0,13):
                self.outFile.write("Nbr of trans type " + myTransNames.getTransformationName(i) +
                                   " is ," + str(transTtlsList[i]) +"\r")
            #outFile.write( "Total number of anti-transformations:  ," + str(ttlAntiTrans)+" \r")
            self.outFile.write("\n\r")
            for i in range(1,9):
                if (myTransNames.getTransformationName(i) != ""):
                    self.outFile.write( "Nbr of anti-trans type "+
                                        myTransNames.getTransformationName(-i) + " is ," +
                                        str(antiTransTtlsList[i]) +"\r")
            
            self.outFile.write( "\n\r Total lines of code:  ," + str(ttlLOC)+" \n\r")
            if ttlComm > 0:
                self.outFile.write( "Avg Trans per commit: , "+ str(ttlTrans/ttlComm)+" \r")
                self.outFile.write( "Avg loc per commit:  ,"+ str(ttlLOC/ttlComm)+" \n\r")

        assignment = assignment + 1
        self.outFile.close()
    
    
    
    
    def printIndividualTotalsAndCountAssignmentTotals(self, myDir, analysisRoot, printToFile, myTrans):
        myGitFile = GitFile.GitFile()
        for item in myDir:
            #print item
            if os.path.isfile(os.path.join(analysisRoot, item)):
                fileName, ext = os.path.splitext(item)
                studentName = fileName.split("_")
                print 'Processing ' + studentName[0]
                if ext == ".gitdata":
                    currentGitFile = myGitFile.retrieveGitReportObject(analysisRoot + os.sep + fileName)
                    if (currentGitFile != None):
                        AssignmentTotals.AssignmentTotals.set_total_submissions(1)
                        studentSubmissionTotals = AssignmentTotals.AssignmentTotals()
        
                        myAssignments = currentGitFile.getAssignments()
                            
                        for myAssignment in myAssignments:
                            myCommitStatsList = myAssignment.get_my_commit_totals()
                            myCommitList = myAssignment.get_my_commits()
                            '''
                            myTransformationsByTranType = myAssignment.get_trans_totals_by_tran_type()
                            myAntiTransformationsByTranType = myAssignment.get_antitrans_totals_by_tran_type() 
                            '''
                            for myCommitStats in myCommitStatsList:
                                AssignmentTotals.AssignmentTotals.set_total_commits(myCommitStats.nbrCommits)
                                
                                studentSubmissionTotals.set_rlcommit(myCommitStats.get_rlcommit())
                                #if myCommitStats.
                                studentSubmissionTotals.set_glcommit(myCommitStats.get_glcommit())
                                studentSubmissionTotals.set_nbr_commits(myCommitStats.get_nbr_commits())
                                studentSubmissionTotals.set_other_commit(myCommitStats.get_other_commit())
                                studentSubmissionTotals.set_ref_commit(myCommitStats.get_ref_commit())

                                studentSubmissionTotals.set_added_lines_in_assignment(myCommitStats.get_added_lines_in_assignment())
                                studentSubmissionTotals.set_added_test_locin_assignment(myCommitStats.get_added_test_locin_assignment())
                                studentSubmissionTotals.set_deleted_lines_in_assignment(myCommitStats.get_deleted_lines_in_assignment())
                                studentSubmissionTotals.set_deleted_test_locin_assignment(myCommitStats.get_deleted_test_locin_assignment())
                                studentSubmissionTotals.set_total_trans_by_type_in_assignment(myCommitStats.get_total_trans_by_type_in_assignment())
                                studentSubmissionTotals.set_total_anti_trans_by_type_in_assignment(myCommitStats.get_total_anti_trans_by_type_in_assignment())
                                
                                self.outFile.write(fileName + ext + "," + str(myAssignment.assignmentName) + "," +
                                                    # format(myAssignment.TDDGrade, '.2f') + "," +
                                                    str(myCommitStats.get_ideal_number_of_cycles()) + "," +
                                                    str(myAssignment.getTDDCycleCount()) + "," +
                                                    str(myAssignment.get_nbr_valid_cycles()) + ", " +
                                                    str(myCommitStats.nbrCommits) + "," +
                                                    str(myCommitStats.RLCommit) + "," +
                                                    str(myCommitStats.get_invalid_rl_commits()) + "," +
                                                    str(myAssignment.getConsecutiveRedLights()) + "," +
                                                    str(myAssignment.getReasonsForConsecutiveCommits("Red Light")) + "," +
                                                    str(myCommitStats.GLCommit) + "," +
                                                    str(myCommitStats.get_invalid_gl_commits()) + "," +
                                                    str(myAssignment.getConsecutiveGreenLights()) + "," +
                                                    str(myAssignment.getReasonsForConsecutiveCommits("Green Light")) + "," +
                                                    str(myCommitStats.refCommit) + "," +
                                                    str(myCommitStats.otherCommit) + "," +
                                                    format(myCommitStats.get_avg_lines_per_commit(), '.2f') + "," +
                                                    format(myCommitStats.get_avg_trans_per_commit(), '.2f') + " ," +
                                                    format(myCommitStats.get_ratio_prod_to_test(), '.2f') + "," +
                                                    str(myCommitStats.addedLinesInAssignment) + "," +
                                                    str(myCommitStats.addedTestLOCInAssignment) + "," +
                                                    str(myCommitStats.deletedLinesInAssignment) + "," +
                                                    str(myCommitStats.deletedTestLOCInAssignment)+ "\r")

                            for myCommit in myCommitList:
                                AssignmentTotals.AssignmentTotals.set_total_nbr_transformations(myCommit.get_number_of_transformations())
                                AssignmentTotals.AssignmentTotals.set_total_nbr_transformations(myCommit.get_number_of_transformations())
                                AssignmentTotals.AssignmentTotals.set_total_prod_files(myCommit.get_nbr_prod_files())
                                AssignmentTotals.AssignmentTotals.set_total_test_files(myCommit.get_nbr_test_files())
                                AssignmentTotals.AssignmentTotals.set_total_LOC(myCommit.get_added_lines_in_commit()+myCommit.get_added_test_loc())
                                AssignmentTotals.AssignmentTotals.set_total_prod_LOC(myCommit.get_added_lines_in_commit()-myCommit.get_deleted_lines_in_commit())
                                AssignmentTotals.AssignmentTotals.set_total_test_LOC(myCommit.get_added_test_loc()-myCommit.get_deleted_test_loc())
                                myFiles = myCommit.get_file_list()
                                for myFile in myFiles:
                                    myTrans = myFile.get_transformations()
                                    for myTran in myTrans:
                                        if myTran >= 0:
                                            AssignmentTotals.AssignmentTotals.set_total_trans_by_type(1 ,myTran)

                                        else:
                                            AssignmentTotals.AssignmentTotals.set_total_antitrans_by_type(1, abs(myTran))
                        self.outFile.write("Totals for " + studentName[0] + "," + str(len(myAssignments)) + ",,,," +
                                            str(studentSubmissionTotals.nbrCommits) + "," +
                                            str(studentSubmissionTotals.RLCommit) + ",,,,,,," +
                                            str(studentSubmissionTotals.GLCommit) + ",,,,,,," +
                                            str(studentSubmissionTotals.refCommit) + "," +
                                            str(studentSubmissionTotals.otherCommit) + "," +
                                            format(studentSubmissionTotals.get_avg_lines_per_commit(), '.2f') + "," +
                                            format(studentSubmissionTotals.get_avg_trans_per_commit(), '.2f') + "," +
                                            format(studentSubmissionTotals.get_ratio_prod_to_test(), '.2f') + "," +
                                            str(studentSubmissionTotals.addedLinesInAssignment) + "," +
                                            str(studentSubmissionTotals.addedTestLOCInAssignment) + "," +
                                            str(studentSubmissionTotals.deletedLinesInAssignment) + "," +
                                            str(studentSubmissionTotals.deletedTestLOCInAssignment)+ "\r\r")

        #return studentSubmissionTotals
       

if __name__ == '__main__':
    myReport = AnalysisReport()
    myReport.createAnalysisReport("/Users/shammond/Google Drive/6700Spring17","/Users/shammond/Google Drive/6700Spring17/Assignment5","yes","Assignment5")
