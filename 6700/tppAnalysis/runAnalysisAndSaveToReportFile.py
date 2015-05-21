'''
Created on Sep 12, 2014

@author: susanha
'''
import os
import printResults
import subprocess
import Transformations


if __name__ == '__main__':
    
    myDrive = "g:\\"
    myDirectory = "Assignment4"
    myAssignment = "CA04"
    '''
    for root, myDir, files in os.walk("c:\\Users\\susanha\\git\\6700Fall14\\"+myDirectory+"\\submissions"):
        nameSplit = root.split("\\")
        for currentDir in myDir:
            if currentDir.endswith(".git"):
                #os.chdir(myDir)
                #print nameSplit[7], "Git directory", os.path.join(root,currentDir)
                os.chdir(os.path.join(root,currentDir))
                p=subprocess.Popen(["git","log","-p","-m","--reverse","--pretty=format:\"%s\""],stdout=subprocess.PIPE)
                outFile = open("c:\\Users\\susanha\\git\\6700Fall14\\"+myDirectory+"\\"+nameSplit[7]+"Log", "w")
                for line in p.stdout.readlines():
                    outFile.write(line)
                outFile.close()
                # print p
        #else:
        #    print "No git folder in " + root
        #print files
    '''
    root = myDrive+"git\\6700Fall14\\"+myDirectory
    myDir = os.listdir(root)
    myResults = printResults.Results(myAssignment)
    outFile = open(myDrive+"git\\6700Fall14\\Report"+myDirectory,"w")
    outFile.write( "Submission name\tNumber of Commits\tAverage Lines Per Commit\tAverage Transformations Per Commit\tRatio of Test to Prod Code\tOverall Deleted Lines \r")
    myTransNames = Transformations.Trans()
    for item in myDir:
        #print item
        if os.path.isfile(os.path.join(root,item)):
            fileName, ext = os.path.splitext(item)
            #print fileName
            if ext == "":
                nbrCommits, avgLinesPerCommit, avgTransPerCommit, ratio, allDeletedLines = myResults.printResults(root,fileName)
                outFile.write( fileName + ext + "\t" + str(nbrCommits) + "\t" + format(avgLinesPerCommit,'.2f') + "\t" + 
                               format(avgTransPerCommit,'.2f')+" \t" + format(ratio,'.2f') +"\t" + str(allDeletedLines) +"\r")
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
    outFile.write( "Average Transformations per commit: \t "+ str(myResults.totalTransformations/myResults.totalCommits)+" \r")
    outFile.write( "Average lines of code per commit:  \t"+ str(myResults.totalLinesOfCode/myResults.totalCommits)+" \n\r")
