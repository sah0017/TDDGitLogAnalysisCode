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


    def readGitFile(self, fileName):
        ## subprocess.call("git log -p -m > logfile")
        myList = []
        gitFile = codecs.open(fileName, encoding='utf-16')
        for line in gitFile:
            if line[0] == '+':
                myList.append('New line')
            if line[0] == '-':
                myList.append('line removed')
            if line.find("Initial") > -1:
                myList.append(myTrans.NEWFILE)
            if line.find("pass") > -1:
                myList.append(myTrans.NULL)
        gitFile.close()
        return myList
    
    def getCommits(self):
        return self.myCommits
    