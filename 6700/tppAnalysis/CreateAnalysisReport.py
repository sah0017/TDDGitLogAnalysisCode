'''
Created on Apr 12, 2016

@author: susanha
'''
import os
import GitFile
import Transformations
import AnalyzeGitLogFileAndCreateRpt
import AssignmentCommitTotals


class AnalysisReport(object):
    pass

    def createAnalysisReport(self, drive,pToF,mySem,myDir):
        myDrive = drive
        printToFile = pToF
        mySemester = mySem
        myDirectory = myDir
        root = myDrive + "git\\" + mySemester + "\\" + myDirectory
        myDir = os.listdir(root)
        myTotals = []
        
        self.outFile = open(myDrive + "git\\" + mySemester + "\\Report" + myDirectory + ".gitrpt", "w")
        myTransNames = Transformations.Trans()
        self.outFile.write("Submission name\tNumber of Assignments\nAssignment Number\tNumber of Commits\tRed Light\tGreen Light\tRefactor\tOther\tAverage Lines Per Commit\tAverage Transformations Per Commit\tRatio of Test to Prod Code\tOverall Deleted/Modified Lines \r")

        myTotals = self.printIndividualTotalsAndCountAssignmentTotals(myDir, root, printToFile, myTotals, myTransNames)
        
        assignment = 1
        #for myAssignmentStats in myTotals:
            
        ttlSub = AssignmentCommitTotals.AssignmentCommitTotals.get_total_submissions()
        ttlComm = AssignmentCommitTotals.AssignmentCommitTotals.get_total_commits()
        ttlTrans = AssignmentCommitTotals.AssignmentCommitTotals.get_total_nbr_transformations()
        transTtlsList = AssignmentCommitTotals.AssignmentCommitTotals.get_total_trans_by_type()
        #ttlAntiTrans = myAssignmentStats.get_total_anti_transformations()
        antiTransTtlsList = AssignmentCommitTotals.AssignmentCommitTotals.get_total_antitrans_by_type()
        ttlLOC = AssignmentCommitTotals.AssignmentCommitTotals.get_total_LOC()
        if printToFile:
            self.outFile.write( "\n\r\n\rAssignment report"+" \n\r")
            self.outFile.write("Assignment:  \t" + str(assignment)+"\n\r")
            self.outFile.write( "Total submissions analyzed:  \t" + str(ttlSub)+" \n\r")
            self.outFile.write( "Total number of commits:  \t" + str(ttlComm)+" \r")
            self.outFile.write( "Total number of transformations:  \t" + str(ttlTrans)+" \r")
            for i in range(0,13):
                self.outFile.write("Number of transformation type " + myTransNames.getTransformationName(i) + " is \t" + str(transTtlsList[i]) +"\r")
            #outFile.write( "Total number of anti-transformations:  \t" + str(ttlAntiTrans)+" \r")
            self.outFile.write("\n\r")
            for i in range(1,9):
                if (myTransNames.getTransformationName(i) != ""):
                    self.outFile.write( "Number of anti-transformation type "+ myTransNames.getTransformationName(-i) + " is \t" + str(antiTransTtlsList[i]) +"\r")
            
            self.outFile.write( "\n\r Total lines of code:  \t" + str(ttlLOC)+" \n\r")
            if ttlComm > 0:
                self.outFile.write( "Average Transformations per commit: \t "+ str(ttlTrans/ttlComm)+" \r")
                self.outFile.write( "Average lines of code per commit:  \t"+ str(ttlLOC/ttlComm)+" \n\r")
        else:
            print "Final report"
            print "Assignment:  ",assignment
            print "Total submissions analyzed:  ",ttlSub
            print "Total number of commits:  ",ttlComm
            print "Total number of transformations:  ", ttlTrans
            for i in range(0,13):
                print "Number of transformation type",i,transTtlsList[i]
            #print "Total number of anti-transformations:  ", ttlAntiTrans
            for i in range(0,9):
                print "Number of anti-transformation type",i,antiTransTtlsList[i]
            
            print "Total lines of code:  ", ttlLOC
            print "Average Transformations per commit:  ", ttlTrans/ttlComm
            print "Average lines of code per commit:  ",ttlLOC/ttlComm
            
        assignment = assignment + 1
    
    
    
    
    
    def printIndividualTotalsAndCountAssignmentTotals(self, myDir, root, printToFile, myTotals, myTrans):
        myGitFile = GitFile.GitFile()
        #myAssignmentTotals = AssignmentCommitTotals.AssignmentCommitTotals()
        for item in myDir:
            #print item
            if os.path.isfile(os.path.join(root, item)):
                fileName, ext = os.path.splitext(item)
                studentName = fileName.split("_")
                #print fileName
                if ext == ".gitdata":
                    currentGitFile = myGitFile.retrieveGitReportObject(root + "\\" + fileName)
                    if (currentGitFile != None):
                        AssignmentCommitTotals.AssignmentCommitTotals.set_total_submissions(1)
        
                        myAssignments = currentGitFile.getAssignments()
                        if printToFile:
                            self.outFile.write(studentName[0] + "\t" + str(len(myAssignments)) + "\n")
                        else:
                            print studentName[0], len(myAssignments)
                            
                        for myAssignment in myAssignments:
                            myCommitStatsList = myAssignment.get_my_commit_totals()
                            myCommitList = myAssignment.get_my_commits()
                            '''
                            myTransformationsByTranType = myAssignment.get_trans_totals_by_tran_type()
                            myAntiTransformationsByTranType = myAssignment.get_antitrans_totals_by_tran_type() 
                            '''
                            for myCommitStats in myCommitStatsList:
                                AssignmentCommitTotals.AssignmentCommitTotals.set_total_commits(myCommitStats.nbrCommits)
                                '''
                                myAssignmentTotals.set_rlcommit(myCommitStats.get_rlcommit())
                                myAssignmentTotals.set_nbr_commits(myCommitStats.get_nbr_commits())
                                myAssignmentTotals.set_other_commit(myCommitStats.get_other_commit())
                                myAssignmentTotals.set_total_del_lines(myCommitStats.get_deleted_lines_in_commit())
                                myAssignmentTotals.set_ref_commit(myCommitStats.get_ref_commit())
                                '''
                                if printToFile:
                                    self.outFile.write(fileName + ext + "\t" + str(myCommitStats.nbrCommits) + "\t" + str(myCommitStats.RLCommit) + "\t" + str(myCommitStats.GLCommit) + "\t" + str(myCommitStats.refCommit) + "\t" + str(myCommitStats.otherCommit) + "\t" + format(myCommitStats.avgLinesPerCommit, '.2f') + "\t" + format(myCommitStats.avgTransPerCommit, '.2f') + " \t" + format(myCommitStats.ratioTestToProd, '.2f') + "\t" + str(myCommitStats.totalDelLines) + "\r")
                                else:
                                    print fileName, ext, myCommitStats.get_nbr_commits, myCommitStats.get_avg_lines_per_commit, myCommitStats.get_avg_trans_per_commit
                            
                            for myCommit in myCommitList:
                                AssignmentCommitTotals.AssignmentCommitTotals.set_total_nbr_transformations(myCommit.get_number_of_transformations())
                                AssignmentCommitTotals.AssignmentCommitTotals.set_total_prod_files(myCommit.get_nbr_prod_files())
                                AssignmentCommitTotals.AssignmentCommitTotals.set_total_test_files(myCommit.get_nbr_test_files())
                                AssignmentCommitTotals.AssignmentCommitTotals.set_total_LOC(myCommit.get_added_lines_in_commit()+myCommit.get_added_test_loc())
                                AssignmentCommitTotals.AssignmentCommitTotals.set_total_prod_LOC(myCommit.get_added_lines_in_commit()-myCommit.get_deleted_lines_in_commit())
                                AssignmentCommitTotals.AssignmentCommitTotals.set_total_test_LOC(myCommit.get_added_test_loc()-myCommit.get_deleted_test_loc())
                                myTrans = myCommit.get_transformations()
                                for myTran in myTrans:
                                    if myTran >= 0:
                                        AssignmentCommitTotals.AssignmentCommitTotals.set_total_trans_by_type(1 ,myTran)
                                        
                                    else:
                                        AssignmentCommitTotals.AssignmentCommitTotals.set_total_antitrans_by_type(1, abs(myTran))
                                        
                            
                                
                            
                            
                            #myTotals.append(myAssignmentTotals)
        return myTotals
       

if __name__ == '__main__':
    myReport = AnalysisReport()
    myReport.createAnalysisReport("g:\\","yes","6700Spring16","CA03")