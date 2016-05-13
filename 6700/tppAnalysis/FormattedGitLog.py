'''
Created on Apr 16, 2016

@author: susanha
'''
import os
import subprocess

class FormattedGitLog(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def formatGitLogOutput(self, root, currentDir, myDrive, mySemester, myDirectory,whichOne):
        os.chdir(os.path.join(root, currentDir))
        p = subprocess.Popen(["git", "whatchanged", "-p", "-m", "--reverse", "--pretty=format:\"commit %h%n%ad%n%s\""], stdout=subprocess.PIPE)
        outFile = open(myDrive + "git\\" + mySemester + "\\" + myDirectory + "\\" + whichOne + "Log.gitdata", "w")
        for line in p.stdout.readlines():
            outFile.write(line)
        
        outFile.close()

    def createFormattedGitLogOutput(self,myDrive, mySemester, myDirectory,whichOne):
        if whichOne == "all":
            for root, myDir, files in os.walk(myDrive + "git\\" + mySemester + "\\" + myDirectory + "\\submissionsLate"):
                nameSplit = root.split("\\")
                for currentDir in myDir:
                    if currentDir.endswith(".git"):
                        #os.chdir(myDir)
                        print nameSplit[4], "Git directory", os.path.join(root, currentDir)
                        self.formatGitLogOutput(root, currentDir,myDrive, mySemester, myDirectory,nameSplit[5])
        else:
            self.formatGitLogOutput(root,currentDir,myDrive, mySemester, myDirectory,whichOne)               
                    # print p
            #else:
            #    print "No git folder in " + root
            #print files   