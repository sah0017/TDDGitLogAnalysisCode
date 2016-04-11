'''
Created on Sep 12, 2014

@author: susanha
'''
import os
import AnalyzeAGitFileAndCreategitoutFile
import subprocess
import Transformations
import Assignment


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
    myResults = AnalyzeAGitFileAndCreategitoutFile.Results()
    outFile = open(myDrive+"git\\"+mySemester+"\\Report"+myDirectory,"w")
    outFile.write( "Submission name\tNumber of Commits\tAverage Lines Per Commit\tAverage Transformations Per Commit\tRatio of Test to Prod Code\tOverall Deleted Lines \r")
    myTransNames = Transformations.Trans()
    for item in myDir:
        #print item
        if os.path.isfile(os.path.join(root,item)):
            fileName, ext = os.path.splitext(item)
            #print fileName
            if ext == "":
                nbrCommits, avgLinesPerCommit, avgTransPerCommit, ratio, allDeletedLines = myResults.printResults(root,fileName)
                if printToFile:
                    outFile.write( fileName + ext + "\t" + str(nbrCommits) + "\t" + format(avgLinesPerCommit,'.2f') + "\t" + 
                               format(avgTransPerCommit,'.2f')+" \t" + format(ratio,'.2f') +"\t" + str(allDeletedLines) +"\r")
                else:
                    print fileName, ext, nbrCommits, avgLinesPerCommit, avgTransPerCommit

    if printToFile:
        outFile.write( "\n\r\n\rFinal report"+" \n\r")
        outFile.write( "Total submissions analyzed:  \t" + str(myResults.totalSubmissions)+" \n\r")
        outFile.write( "Total number of commits:  \t" + str(myResults.totalCommits)+" \r")
        outFile.write( "Total number of transformations:  \t" + str(myResults.totalTransformations)+" \r")
        for i in range(0,13):
            outFile.write("Number of transformation type " + myTransNames.myName(i) + " is \t" + str(myResults.transTotals[i]) +"\r")
        outFile.write( "Total number of anti-transformations:  \t" + str(myResults.totalAntiTransformations)+" \r")
        for i in range(0,9):
            if myTransNames.myName != "":
                outFile.write( "Number of anti-transformation type "+ myTransNames.myName(-i) + " is \t" + str(myResults.antitransTotals[i]) +"\r")
        
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
