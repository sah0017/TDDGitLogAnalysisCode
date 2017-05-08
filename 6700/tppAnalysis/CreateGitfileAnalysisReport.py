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

    def createAnalysisReport(self, reportRoot,analysisRoot, pToF, myAssignment):
        printToFile = pToF
        myDir = os.listdir(analysisRoot)
        myAssignmentTotals = []
        
        self.outFile = open(reportRoot + os.sep + "Report" + myAssignment + ".txt", "w")
        myTransNames = Transformations.Trans()
        self.outFile.write("Submission name\tAssignment Name\tNbr of Commits\tRed Light\tGreen Light\tRefactor\tOther\tNbr Consec RL\tNbr Consec GL\tAvg Lines Per Commit\tAvg Trans Per Commit\tRatio-Prod to Test Code\tAdded Prod Lines\tAdded Test Lines\tDel/Mod Lines \tDel/Mod Test Lines\r")

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
            self.outFile.write("Assignment:  \t" + str(assignment)+"\n\r")
            self.outFile.write( "Total submissions analyzed:  \t" + str(ttlSub)+" \n\r")
            self.outFile.write( "Total nbr of commits:  \t" + str(ttlComm)+" \r")
            self.outFile.write( "Total nbr of transformations:  \t" + str(ttlTrans)+" \r")
            for i in range(0,13):
                self.outFile.write("Nbr of trans type " + myTransNames.getTransformationName(i) + " is \t" + str(transTtlsList[i]) +"\r")
            #outFile.write( "Total number of anti-transformations:  \t" + str(ttlAntiTrans)+" \r")
            self.outFile.write("\n\r")
            for i in range(1,9):
                if (myTransNames.getTransformationName(i) != ""):
                    self.outFile.write( "Nbr of anti-trans type "+ myTransNames.getTransformationName(-i) + " is \t" + str(antiTransTtlsList[i]) +"\r")
            
            self.outFile.write( "\n\r Total lines of code:  \t" + str(ttlLOC)+" \n\r")
            if ttlComm > 0:
                self.outFile.write( "Avg Trans per commit: \t "+ str(ttlTrans/ttlComm)+" \r")
                self.outFile.write( "Avg loc per commit:  \t"+ str(ttlLOC/ttlComm)+" \n\r")
        else:
            print "Final report"
            print "Assignment:  ",assignment
            print "Total submissions analyzed:  ",ttlSub
            print "Total number of commits:  ",ttlComm
            print "Total number of transformations:  ", ttlTrans
            for i in range(0,13):
                print "Nbr of trans type",i,transTtlsList[i]
            #print "Total number of anti-transformations:  ", ttlAntiTrans
            for i in range(0,9):
                print "Nbr of anti-trans type",i,antiTransTtlsList[i]
            
            print "Total lines of code:  ", ttlLOC
            print "Avg Trans per commit:  ", format(ttlTrans/ttlComm, '.2f')
            print "Avg loc per commit:  ",format(ttlLOC/ttlComm, '.2f')
            
        assignment = assignment + 1
        self.outFile.close()
    
    
    
    
    def printIndividualTotalsAndCountAssignmentTotals(self, myDir, analysisRoot, printToFile, myTrans):
        myGitFile = GitFile.GitFile()
        for item in myDir:
            #print item
            if os.path.isfile(os.path.join(analysisRoot, item)):
                fileName, ext = os.path.splitext(item)
                studentName = fileName.split("_")
                #print fileName
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
                                
                                if printToFile:
                                    self.outFile.write(fileName + ext + "\t" + str(myAssignment.assignmentName) + "\t" + str(myCommitStats.nbrCommits) + "\t" + str(myCommitStats.RLCommit) + "\t" + str(myCommitStats.GLCommit) + 
                                                       "\t" + str(myCommitStats.refCommit) + "\t" + str(myCommitStats.otherCommit) + "\t" + str(myAssignment.getConsecutiveRedLights()) + "\t" +
                                                        str(myAssignment.getConsecutiveGreenLights()) + "\t" + format(myCommitStats.get_avg_lines_per_commit(), '.2f') +
                                                       "\t" + format(myCommitStats.get_avg_trans_per_commit(), '.2f') + " \t" + format(myCommitStats.get_ratio_prod_to_test(), '.2f') + "\t" + 
                                                       str(myCommitStats.addedLinesInAssignment) + "\t" + str(myCommitStats.addedTestLOCInAssignment) + "\t" + 
                                                       str(myCommitStats.deletedLinesInAssignment) + "\t" + str(myCommitStats.deletedTestLOCInAssignment)+ "\r")
                                else:
                                    print fileName, ext, myCommitStats.get_nbr_commits, myCommitStats.get_avg_lines_per_commit(), myCommitStats.get_avg_trans_per_commit()
                            
                            for myCommit in myCommitList:
                                AssignmentTotals.AssignmentTotals.set_total_nbr_transformations(myCommit.get_number_of_transformations())
                                AssignmentTotals.AssignmentTotals.set_total_prod_files(myCommit.get_nbr_prod_files())
                                AssignmentTotals.AssignmentTotals.set_total_test_files(myCommit.get_nbr_test_files())
                                AssignmentTotals.AssignmentTotals.set_total_LOC(myCommit.get_added_lines_in_commit()+myCommit.get_added_test_loc())
                                AssignmentTotals.AssignmentTotals.set_total_prod_LOC(myCommit.get_added_lines_in_commit()-myCommit.get_deleted_lines_in_commit())
                                AssignmentTotals.AssignmentTotals.set_total_test_LOC(myCommit.get_added_test_loc()-myCommit.get_deleted_test_loc())
                                myTrans = myCommit.get_transformations()
                                for myTran in myTrans:
                                    if myTran >= 0:
                                        AssignmentTotals.AssignmentTotals.set_total_trans_by_type(1 ,myTran)
                                        
                                    else:
                                        AssignmentTotals.AssignmentTotals.set_total_antitrans_by_type(1, abs(myTran))
                        if printToFile:
                            self.outFile.write("Totals for " + studentName[0] + "\t" + str(len(myAssignments)) + "\t" + str(studentSubmissionTotals.nbrCommits) + "\t" + str(studentSubmissionTotals.RLCommit) + "\t" + str(studentSubmissionTotals.GLCommit) + 
                                                       "\t" + str(studentSubmissionTotals.refCommit) + "\t" + str(studentSubmissionTotals.otherCommit) + "\t" + format(studentSubmissionTotals.get_avg_lines_per_commit(), '.2f') + 
                                                       "\t" + format(studentSubmissionTotals.get_avg_trans_per_commit(), '.2f') + " \t" + format(studentSubmissionTotals.get_ratio_prod_to_test(), '.2f') + "\t" + 
                                                       str(studentSubmissionTotals.addedLinesInAssignment) + "\t" + str(studentSubmissionTotals.addedTestLOCInAssignment) + "\t" + 
                                                       str(studentSubmissionTotals.deletedLinesInAssignment) + "\t" + str(studentSubmissionTotals.deletedTestLOCInAssignment)+ "\r\r")
                        else:
                            print studentName[0], len(myAssignments)

        #return studentSubmissionTotals
       

if __name__ == '__main__':
    myReport = AnalysisReport()
    myReport.createAnalysisReport("/Users/shammond/Google Drive/6700Spring17","/Users/shammond/Google Drive/6700Spring17/Assignment5","yes","Assignment5")
