'''
Created on Jul 10, 2014

@author: susanha
'''

import subprocess
import Transformations
import codecs
import Commit
import File

myTrans = Transformations.Trans() 


class GitFile(object):
 
   
    
    def __init__(self):
        '''
        Constructor
        '''
        self.myCommits = []
        self.myTransformations = []
        self.myFiles = []


    def readGitFile(self, fileName):
        ## subprocess.call("git log -p -m > logfile")
        
        gitFile = codecs.open(fileName, encoding='utf-16')
        for line in gitFile:
            if line[0] == '+':
                self.myTransformations.append('New line')
            if line[0] == '-':
                self.myTransformations.append('line removed')
            if line.find("Initial") > -1:
                self.myTransformations.append(myTrans.NEWFILE)
                self.newCommit = Commit.Commit()
                self.myCommits.append(self.newCommit)
            if (line.find("green")) > -1:
                self.newCommit = Commit.Commit()
                self.myCommits.append(self.newCommit)
            if line.find("pass") > -1:
                self.myTransformations.append(myTrans.NULL)
            if line.find('--- /dev/null') > -1:
                line = gitFile.readline()
                strLine = line.rstrip()
                if strLine.endswith(".py"):
                    splLine = strLine.split("/")
                    self.newFile = File.File(splLine[len(splLine)-1])
                    self.myFiles.append(self.newFile)
                
        gitFile.close()

    
    def getCommits(self):
        return self.myCommits
    
    def getTransformations(self):
        return self.myTransformations
    
    def getFiles(self):
        return self.myFiles
    