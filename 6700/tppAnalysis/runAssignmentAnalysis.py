'''
Created on Sep 12, 2014

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

            
    for root, myDir, files in os.walk(myDrive+"git\\"+mySemester+"\\"+myDirectory+"\\submissionsLate"):
        nameSplit = root.split("\\")
        for currentDir in myDir:
            if currentDir.endswith(".git"):
                #os.chdir(myDir)
                print nameSplit[4], "Git directory", os.path.join(root,currentDir)
                os.chdir(os.path.join(root,currentDir))
                p=subprocess.Popen(["git","whatchanged","-p","-m","--reverse","--pretty=format:\"commit %h%n%ad%n%s\""],stdout=subprocess.PIPE)
                outFile = open(myDrive+"git\\"+mySemester+"\\"+myDirectory+"\\"+nameSplit[5]+"Log", "w")
                for line in p.stdout.readlines():
                    outFile.write(line)
                outFile.close()
                # print p
        #else:
        #    print "No git folder in " + root
        #print files
         
    root = myDrive+"git\\"+mySemester+"\\"+myDirectory
    myDir = os.listdir(root)
    myResults = AnalyzeAGitLogFileAndCreateGitoutFile.Results()
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
                    outFile.write( fileName + ext + "\t" + str(myCommitStats.get_nbr_commits()) + "\t" 
                                   + str(myCommitStats.get_rlcommit()) + "\t" + str(myCommitStats.get_glcommit()) + "\t"+ str(myCommitStats.get_ref_commit()) + "\t"
                                   + str(myCommitStats.get_other_commit()) + "\t" + format(myCommitStats.get_avg_trans_per_commit(),'.2f') + "\t" + 
                               format(myCommitStats.get_avg_trans_per_commit(),'.2f')+" \t" + format(myCommitStats.get_ratio_test_to_prod(),'.2f') +"\t" + str(myCommitStats.get_avg_lines_per_commit()) +"\r")
                else:
                    print fileName, ext, myCommitStats.get_nbr_commits(), myCommitStats.get_avg_lines_per_commit(), myCommitStats.get_avg_trans_per_commit()
    
    ttlSub = myResults.get_total_submissions()
    ttlComm = myResults.get_total_commits()
    ttlTrans = myResults.get_total_transformations()
    transTtlsList = myResults.get_trans_totals()
    ttlAntiTrans = myResults.get_total_anti_transformations()
    antiTransTtlsList = myResults.get_antitrans_totals()
    ttlLOC = myResults.get_total_lines_of_code()
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
        if myResults.totalCommits > 0:
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
