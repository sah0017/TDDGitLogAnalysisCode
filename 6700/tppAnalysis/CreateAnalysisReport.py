'''
Created on Apr 12, 2016

@author: susanha
'''
import os
import AnalyzeAGitLogFileAndCreateGitoutFile
import subprocess
import Transformations
import Assignment
import AssignmentCommitTotals


if __name__ == '__main__':
    myDrive = "g:\\"
    printToFile = raw_input("Print output to file?  ")
    mySemester = "6700Spring16"
    myDirectory = "CA02"
         
    root = myDrive+"git\\"+mySemester+"\\"+myDirectory
    myDir = os.listdir(root)
    myTransNames = Transformations.Trans()
    myGitFile = GitFile.GitFile(root+"\\"+fileName)
    myResults = myGitfile.retrieveGitoutFileObject(root+"\\"+fileName)
    outFile = open(myDrive+"git\\"+mySemester+"\\Report"+myDirectory,"w")
    outFile.write( "Submission name\tNumber of Commits\tRed Light\tGreen Light\tRefactor\tOther\tAverage Lines Per Commit\tAverage Transformations Per Commit\tRatio of Test to Prod Code\tOverall Deleted Lines \r")
    myTransNames = Transformations.Trans()
    for item in myDir:
        #print item
        if os.path.isfile(os.path.join(root,item)):
            fileName, ext = os.path.splitext(item)
            #print fileName
            if ext == "":
                myCommitStats = myResults.analyzeGitLog(root,fileName)
                if printToFile:
                    outFile.write( fileName + ext + "\t" + str(myCommitStats.nbrCommits) + "\t" 
                                   + str(myCommitStats.RLCommit) + "\t" + str(myCommitStats.GLCommit) + "\t"+ str(myCommitStats.refCommit) + "\t"
                                   + str(myCommitStats.otherCommit) + "\t" + format(myCommitStats.avgLinesPerCommit,'.2f') + "\t" + 
                               format(myCommitStats.avgTransPerCommit,'.2f')+" \t" + format(myCommitStats.ratioTestToProd,'.2f') +"\t" + str(myCommitStats.avgLinesPerCommit) +"\r")
                else:
                    print fileName, ext, myCommitStats.nbrCommits, myCommitStats.avgLinesPerCommit, myCommitStats.avgTransPerCommit
    
    if printToFile:
        outFile.write( "\n\r\n\rFinal report"+" \n\r")
        outFile.write( "Total submissions analyzed:  \t" + str(myResults.totalSubmissions)+" \n\r")
        outFile.write( "Total number of commits:  \t" + str(myResults.totalCommits)+" \r")
        outFile.write( "Total number of transformations:  \t" + str(myResults.totalTransformations)+" \r")
        for i in range(0,13):
            outFile.write("Number of transformation type " + myTransNames.getTransformationName(i) + " is \t" + str(myResults.transTotals[i]) +"\r")
        outFile.write( "Total number of anti-transformations:  \t" + str(myResults.totalAntiTransformations)+" \r")
        for i in range(0,9):
            if myTransNames.getTransformationName != "":
                outFile.write( "Number of anti-transformation type "+ myTransNames.getTransformationName(-i) + " is \t" + str(myResults.antitransTotals[i]) +"\r")
        
        outFile.write( "Total lines of code:  \t" + str( myResults.totalLinesOfCode)+" \n\r")
        if myResults.totalCommits > 0:
            outFile.write( "Average Transformations per commit: \t "+ str(myResults.totalTransformations/myResults.totalCommits)+" \r")
            outFile.write( "Average lines of code per commit:  \t"+ str(myResults.totalLinesOfCode/myResults.totalCommits)+" \n\r")
    else:
        print "Final report"
        print "Total submissions analyzed:  ",myResults.totalSubmissions
        print "Total number of commits:  ",myResults.totalCommits
        print "Total number of transformations:  ", myResults.totalTransformations
        for i in range(0,13):
            print "Number of transformation type",i,myResults.transTotals[i]
        print "Total number of anti-transformations:  ", myResults.totalAntiTransformations
        for i in range(0,9):
            print "Number of anti-transformation type",i,myResults.antitransTotals[i]
        
        print "Total lines of code:  ", myResults.totalLinesOfCode
        print "Average Transformations per commit:  ", myResults.totalTransformations/myResults.totalCommits
        print "Average lines of code per commit:  ",myResults.totalLinesOfCode/myResults.totalCommits
