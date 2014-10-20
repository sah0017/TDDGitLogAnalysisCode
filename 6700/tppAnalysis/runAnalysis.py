'''
Created on Sep 12, 2014

@author: susanha
'''
import os
import printResults
import subprocess

if __name__ == '__main__':

    for root, dir, files in os.walk("c:\\Users\\susanha\\git\\6700Fall14\\Assignment2\\submissions"):
        nameSplit = root.split("\\")
        for currentDir in dir:
            if currentDir.endswith(".git"):
                #os.chdir(dir)
                #print nameSplit[7], "Git directory", os.path.join(root,currentDir)
                os.chdir(os.path.join(root,currentDir))
                p=subprocess.Popen(["git","log","-p","-m","--reverse","--pretty=format:\"%s\""],stdout=subprocess.PIPE)
                outFile = open("c:\\Users\\susanha\\git\\6700Fall14\\Assignment2\\"+nameSplit[7]+"Log", "w")
                for line in p.stdout.readlines():
                    outFile.write(line)
                outFile.close()
                # print p
        #else:
        #    print "No git folder in " + root
        #print files
    root = "c:\\Users\\susanha\\git\\6700Fall14\\Assignment2"
    dir = os.listdir(root)
    myResults = printResults.Results()
    for item in dir:
        #print item
        if os.path.isfile(os.path.join(root,item)):
            fileName, ext = os.path.splitext(item)
            #print fileName
            if ext == "":
                nbrCommits, avgLinesPerCommit, avgTransPerCommit = myResults.printResults(root,fileName)
                print fileName, ext, nbrCommits, avgLinesPerCommit, avgTransPerCommit
    print "Final report"
    print "Total submissions analyzed:  ",myResults.totalSubmissions
    print "Total number of commits:  ",myResults.totalCommits
    print "Total number of transformations:  ", myResults.totalTransformations
    print "Total number of anti-transformations:  ", myResults.totalAntiTransformations
    
    print "Total lines of code:  ", myResults.totalLinesOfCode
    print "Average Transformations per commit:  ", myResults.totalTransformations/myResults.totalCommits
    print "Average lines of code per commit:  ",myResults.totalLinesOfCode/myResults.totalCommits
