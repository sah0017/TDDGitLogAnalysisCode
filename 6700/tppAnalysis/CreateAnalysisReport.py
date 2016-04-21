'''
Created on Apr 12, 2016

@author: susanha
'''
import os
import GitFile
import AnalyzeAGitLogFileAndCreateIndivRpt
import subprocess
import Transformations
import Assignment
import AssignmentCommitTotals


def createAnalysisReport(drive,pToF,mySem,myDir):
    myDrive = drive
    printToFile = pToF
    mySemester = mySem
    myDirectory = myDir
    root = myDrive + "git\\" + mySemester + "\\" + myDirectory
    myDir = os.listdir(root)
    myTransNames = Transformations.Trans()
    myGitFile = GitFile.GitFile()
    outFile = open(myDrive + "git\\" + mySemester + "\\Report" + myDirectory, "w")
    outFile.write("Submission name\tNumber of Assignments\nAssignment Number\tNumber of Commits\tRed Light\tGreen Light\tRefactor\tOther\tAverage Lines Per Commit\tAverage Transformations Per Commit\tRatio of Test to Prod Code\tOverall Deleted Lines \r")
    myTransNames = Transformations.Trans()
    for item in myDir:
        #print item
        if os.path.isfile(os.path.join(root, item)):
            fileName, ext = os.path.splitext(item)
            #print fileName
            if ext == "":
                currentGitFile = myGitFile.retrieveGitReportObject(root + "\\" + fileName)
                myAssignments = currentGitFile.getAssignments 
                if printToFile:
                    outFile.write(fileName + ext + "\t" + str(len(myAssignments)) + "\n")
                else:
                    print fileName, ext, len(myAssignments)
                for myAssignment in myAssignments:
                    myCommitStatsList = myAssignment.get_my_commit_totals
                    for myCommitStats in myCommitStatsList:
                        if printToFile:
                            outFile.write(fileName + ext + "\t" + str(myCommitStats.nbrCommits) + "\t" + str(myCommitStats.RLCommit) + "\t" + str(myCommitStats.GLCommit) + "\t" + str(myCommitStats.refCommit) + "\t" + str(myCommitStats.otherCommit) + "\t" + format(myCommitStats.avgLinesPerCommit, '.2f') + "\t" + format(myCommitStats.avgTransPerCommit, '.2f') + " \t" + format(myCommitStats.ratioTestToProd, '.2f') + "\t" + str(myCommitStats.avgLinesPerCommit) + "\r")
                        else:
                            print fileName, ext, myCommitStats.nbrCommits, myCommitStats.avgLinesPerCommit, myCommitStats.avgTransPerCommit
    
    ttlSub = GitFile.get_total_submissions()
    ttlComm = GitFile.get_total_commits()
    ttlTrans = GitFile.get_total_transformations()
    transTtlsList = GitFile.get_trans_totals()
    ttlAntiTrans = GitFile.get_total_anti_transformations()
    antiTransTtlsList = GitFile.get_antitrans_totals()
    ttlLOC = GitFile.get_total_lines_of_code()
    if printToFile:
        outFile.write( "\n\r\n\rFinal report"+" \n\r")
        outFile.write( "Total submissions analyzed:  \t" + str(ttlSub)+" \n\r")
        outFile.write( "Total number of commits:  \t" + str(ttlComm)+" \r")
        outFile.write( "Total number of transformations:  \t" + str(ttlTrans)+" \r")
        for i in range(0,13):
            outFile.write("Number of transformation type " + myTransNames.getTransformationName(i) + " is \t" + str(transTtlsList[i]) +"\r")
        outFile.write( "Total number of anti-transformations:  \t" + str(ttlAntiTrans)+" \r")
        for i in range(0,9):
            if myTransNames.getTransformationName != "":
                outFile.write( "Number of anti-transformation type "+ myTransNames.getTransformationName(-i) + " is \t" + str(antiTransTtlsList[i]) +"\r")
        
        outFile.write( "Total lines of code:  \t" + str(ttlLOC)+" \n\r")
        if GitFile.totalCommits > 0:
            outFile.write( "Average Transformations per commit: \t "+ str(ttlTrans/ttlComm)+" \r")
            outFile.write( "Average lines of code per commit:  \t"+ str(ttlLOC/ttlComm)+" \n\r")
    else:
        print "Final report"
        print "Total submissions analyzed:  ",ttlSub
        print "Total number of commits:  ",ttlComm
        print "Total number of transformations:  ", ttlTrans
        for i in range(0,13):
            print "Number of transformation type",i,transTtlsList[i]
        print "Total number of anti-transformations:  ", ttlAntiTrans
        for i in range(0,9):
            print "Number of anti-transformation type",i,antiTransTtlsList[i]
        
        print "Total lines of code:  ", ttlLOC
        print "Average Transformations per commit:  ", ttlTrans/ttlComm
        print "Average lines of code per commit:  ",ttlLOC/ttlComm



if __name__ == '__main__':
    createAnalysisReport("g:\\","yes","6700Spring16","CA02","re-run")
