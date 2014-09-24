'''
Created on Sep 12, 2014

@author: susanha
'''
import os
import printResults
import subprocess

if __name__ == '__main__':

    for root, dir, files in os.walk("c:\\Users\\susanha\\git\\6700Fall14\\Assignment1\\submissions"):
        nameSplit = root.split("\\")
        for currentDir in dir:
            if currentDir.endswith(".git"):
                #os.chdir(dir)
                #print nameSplit[7], "Git directory", os.path.join(root,currentDir)
                os.chdir(os.path.join(root,currentDir))
                p=subprocess.Popen(["git","log","-p","-m","--reverse","--pretty=format:\"%s\""],stdout=subprocess.PIPE)
                outFile = open("c:\\Users\\susanha\\git\\6700Fall14\\Assignment1\\"+nameSplit[7]+"Log", "w")
                for line in p.stdout.readlines():
                    outFile.write(line)
                outFile.close()
                # print p
        #else:
        #    print "No git folder in " + root
        #print files
    root = "c:\\Users\\susanha\\git\\6700Fall14\\Assignment1"
    dir = os.listdir(root)
    myResults = printResults.Results()
    outFile = open("c:\\Users\\susanha\\git\\6700Fall14\\ReportAssignment1","w")
    outFile.write( "Submission name\tNumber of Commits\tAverage Lines Per Commit\tAverage Transformations Per Commit \r")
    for item in dir:
        #print item
        if os.path.isfile(os.path.join(root,item)):
            fileName, ext = os.path.splitext(item)
            #print fileName
            if ext == "":
                nbrCommits, avgLinesPerCommit, avgTransPerCommit = myResults.printResults(fileName)
                outFile.write( fileName + ext + "\t" + str(nbrCommits) + "\t" + str(avgLinesPerCommit) + "\t" + str(avgTransPerCommit)+" \r")
    outFile.write( "\n\r\n\rFinal report"+" \n\r")
    outFile.write( "Total submissions analyzed:  \t" + str(myResults.totalSubmissions)+" \n\r")
    outFile.write( "Total number of commits:  \t" + str(myResults.totalCommits)+" \r")
    outFile.write( "Total number of transformations:  \t" + str(myResults.totalTransformations)+" \r")
    outFile.write( "Total number of anti-transformations:  \t" + str(myResults.totalAntiTransformations)+" \r")
    
    outFile.write( "Total lines of code:  \t" + str( myResults.totalLinesOfCode)+" \n\r")
    outFile.write( "Average Transformations per commit: \t "+ str(myResults.totalTransformations/myResults.totalCommits)+" \r")
    outFile.write( "Average lines of code per commit:  \t"+ str(myResults.totalLinesOfCode/myResults.totalCommits)+" \n\r")
