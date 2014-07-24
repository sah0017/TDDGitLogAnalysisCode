'''
Created on Jul 10, 2014

@author: susanha
'''

import subprocess
import Transformations
import codecs
import Commit

myTrans = Transformations.Trans() 


class GitFile(object):
 
   
    
    def __init__(self):
        '''
        Constructor
        '''
        self.myCommits = []
        self.myTransformations = []


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
            if line.find("pass") > -1:
                self.myTransformations.append(myTrans.NULL)
        gitFile.close()

    
    def getCommits(self):
        return self.myCommits
    
    def getTransformations(self):
        return self.myTransformations
    