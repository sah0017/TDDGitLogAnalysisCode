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
 
    line = ''
    
    def __init__(self, fileName):
        '''
        Constructor
        '''
        self.fileName = fileName
        self.myCommits = []
        self.myTransformations = []
        self.myFiles = []
        self.gitFile = ''
        self.commits = 0


    def readGitFile(self):
        ## subprocess.call("git log -p -m > logfile")
        
        self.gitFile = codecs.open(self.fileName, encoding='utf-16')

        ## for the first commit, there are some files python creates that we don't need
        ## this while loop is designed to skip over that stuff.
        self.line = self.gitFile.readline()       ## this should be the first commit comment
        while not self.pythonFileFound(): 
            self.line = self.gitFile.readline()   ## skips over unneccesary lines
        strLine = self.line.rstrip() ## should be on diff line now
        splLine = strLine.split("/") ## split the line to get the file name, it's in the last element of the list
        if (splLine[len(splLine)-1] == '__init__.py'):  ## if they didn't delete the __init__.py file, we don't need that either
            for x in range(0,3):                        ## this for loop skips over __init__ file stuff
                self.line = self.gitFile.readline()
        self.commits = self.commits + 1
        self.analyzeCommit()                    ## we should now be at python files that we want to analyze for the initial commit
        for self.line in self.gitFile:
            self.commits = self.commits + 1
            self.analyzeCommit()
                
        self.gitFile.close()

    def analyzeCommit(self):
        commitAddedLines = 0
        commitDeletedLines = 0
        while self.sameCommit() == True:
            
                
            addedLines, deletedLines = self.analyzeFile()
    
            commitAddedLines = commitAddedLines + addedLines
            commitDeletedLines = commitDeletedLines + deletedLines
        self.newCommit = Commit.Commit(self.commits, commitAddedLines,commitDeletedLines)
        for trans in self.myTransformations:
            self.newCommit.addTransformation(trans)
        self.myCommits.append(self.newCommit)    



    def analyzeFile(self):
        fileAddedLines = 0
        fileDeletedLines = 0
        strLine = self.line.rstrip() ## should be on diff line now
        splLine = strLine.split("/") ## split the line to get the file name, it's in the last element of the list
        fileName = splLine[len(splLine) - 1]
        self.line = self.gitFile.readline() ## either new file mode or index
        if self.line.startswith('new'):
            
            self.newFile = File.File(fileName,self.commits)
            self.myFiles.append(self.newFile)
            self.myTransformations.append(myTrans.NEWFILE)
            self.line = self.gitFile.readline() ## if this was a new file, then advance file pointer to index line
            fileIndex = len(self.myFiles) - 1
        else:
            for x in self.myFiles:
                if x.getFileName() == fileName: 
                    fileIndex = self.myFiles.index(x) 
        for x in range(0, 3): ## skips --- line, +++ line, and @@ line
            self.line = self.gitFile.readline()
        
        fileAddedLines, fileDeletedLines = self.evaluateTransformations()
        self.myFiles[fileIndex].setCommitDetails(self.commits, fileAddedLines, fileDeletedLines)
        return fileAddedLines, fileDeletedLines


        
    def pythonFileFound(self):
        evalLine = self.line.rstrip()
        if ((evalLine.startswith("diff")) and (evalLine.endswith(".py"))):
            return True
        elif self.sameCommit() == False:
            return True
        else:
            return False
           
    def evaluateTransformations(self):
        addedLines = 0
        deletedLines = 0
        while not self.pythonFileFound():   ## this would indicate a new python file within the same commit
            if self.line[0] == '+':
                addedLines = addedLines + 1
            if self.line[0] == '-':
                deletedLines = deletedLines + 1
            if self.line.find("pass") > -1:
                self.myTransformations.append(myTrans.NULL)
            self.line = self.gitFile.readline()
        
        return addedLines, deletedLines

    def sameCommit(self):
        if self.line.find('green') > -1:
            return False
        elif self.line == '':   ## looking for end of file
            return False
        else:
            return True
    
    def getCommits(self):
        return self.myCommits
    
    def getTransformations(self):
        return self.myTransformations
    
    def getFiles(self):
        return self.myFiles
    