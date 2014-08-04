'''
Created on Jul 10, 2014

@author: susanha
'''

import subprocess
import Transformations
import codecs
import Commit
import File
import re

myTrans = Transformations.Trans() 


class GitFile(object):
 
    line = ''
    
    def __init__(self, fileName):
        '''
        Constructor
        '''
        self.fileName = fileName
        self.myCommits = []
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
        testFiles = 0
        prodFiles = 0
        self.myTransformations = []
        while self.sameCommit() == True:
            addedLines, deletedLines, testFile = self.analyzeFile()
            commitAddedLines = commitAddedLines + addedLines
            commitDeletedLines = commitDeletedLines + deletedLines
            if testFile:
                testFiles = testFiles + 1
            else:
                prodFiles = prodFiles + 1
        self.newCommit = Commit.Commit(self.commits, commitAddedLines,commitDeletedLines, testFiles, prodFiles)
        for trans in self.myTransformations:
            self.newCommit.addTransformation(trans)
        self.myCommits.append(self.newCommit)    
   

    def analyzeFile(self):
        fileAddedLines = 0
        fileDeletedLines = 0
        fileName = self.extractFileName()
        testFile = self.isTestFile(fileName)
        self.line = self.gitFile.readline() ## either new file mode or index
        matchObj = re.match('new file mode',self.line)
        if matchObj:
            fileIndex = self.addNewFile(fileName, testFile)
        else:
            fileIndex = self.findExistingFileToAddCommitDetails(fileName) 
        for x in range(0, 3): ## skips --- line, +++ line, and @@ line
            self.line = self.gitFile.readline()
        
        fileAddedLines, fileDeletedLines = self.evaluateTransformations()
        self.myFiles[fileIndex].setCommitDetails(self.commits, fileAddedLines, fileDeletedLines)
        return fileAddedLines, fileDeletedLines, testFile
    



    def evaluateTransformations(self):
        addedLines = 0
        deletedLines = 0
        deletedNullValue = False
        deletedLiteral = False
        deletedIf = False
        deletedWhile = False
        ifContents = []
        whileContents = []
        while not self.pythonFileFound():   ## this would indicate a new python file within the same commit
            if self.line[0] == '-':
                deletedLines = deletedLines + 1
                deletedNullValue = self.checkForDeletedNullValue()
                if re.search("return", self.line):
                    deletedLiteral = self.checkForConstantOnReturn(self.line)
                if re.search(r"\bif .", self.line):
                    deletedIf = True
                    ifConditionalParts = self.line.split("if")
                    ifConditional = ifConditionalParts[1].strip()
                    ifContents.append(ifConditional)
                if re.search(r"\bwhile .", self.line):
                    deletedWhile = True
                    whileConditionalParts = self.line.split("while")
                    whileConditional = whileConditionalParts[1].strip()
                    whileContents.append(whileConditional)
                
            if self.line[0] == '+':
                addedLines = addedLines + 1
                if self.line.find("pass") > -1:
                    self.myTransformations.append(myTrans.NULL)
                if re.search("return", self.line):
                    rtnBoolean, rtnValue = self.returnWithNull()
                    if rtnBoolean == True:
                        self.myTransformations.append(myTrans.NULL)   ## this is either a 'return' or a 'return None'
                    else:
                        ## this looks for constants after 'return'
                        if self.checkForConstantOnReturn(rtnValue):                                     ## if there are constants and
                            if deletedNullValue == True:                ## if there was a Null expression before, they probably did Null to Constant
                                self.myTransformations.append(myTrans.N2C)
                            else:                                       ## if constants but no previous Null, they probably just went straight to constant
                                self.myTransformations.append(myTrans.ConstOnly)
                        else:                                         ## if it wasn't constants on the return
                            if deletedLiteral:                        ## and the delete section removed a 'return' with a constant
                                self.myTransformations.append(myTrans.C2V)    ## then it is probably a constant to variable
                noLeadingPlus = self.line[1:]
                if (re.search(r"\bif .(?!_name__ == \"__main)",self.line)):
                    self.myTransformations.append(myTrans.SF)
                elif (re.search(r"\bwhile\b",self.line)):
                    whileTrans = self.checkWhileForMatchingIfOrWhile(deletedIf, ifContents, deletedWhile, whileContents)
                    self.myTransformations.append(whileTrans)              
                elif (re.search(r"[+/*%\-]|/bmath.",noLeadingPlus)):
                    self.myTransformations.append(myTrans.AComp)
            self.line = self.gitFile.readline()
        
        return addedLines, deletedLines

    def checkWhileForMatchingIfOrWhile(self, deletedIf, ifContents, deletedWhile, delWhileContents):
        whileConditionalParts = self.line.split("while")
        whileCondition = whileConditionalParts[1].strip()
        if deletedIf:
            for cond in ifContents:
                if whileCondition == cond:
                    return myTrans.I2W
                else:
                    whileTrans = myTrans.WhileNoIf
        if deletedWhile:
            for cond in delWhileContents:
                whileTrans = self.checkForConstantToVariableInCondition(cond,whileCondition)
        return whileTrans



    def splitAndCleanCondition(self, cond):
        mySplit = cond.split(" ")
        myfirstcond = mySplit[0]
        mycond = mySplit[1]
        mysecondcond = mySplit[2]
        if myfirstcond.startswith("("):
            myfirstcond = myfirstcond[1:]
        removeTrailingChars = re.search(r"[a-zA-Z0-9_^):]",mysecondcond)
        if removeTrailingChars:
            mysecondcond = removeTrailingChars.group(0)
        return myfirstcond, mycond, mysecondcond

    def checkForConstantToVariableInCondition(self, firstCond, secondCond):
        myfirstIfCond, myIfCond, mysecondIfCond = self.splitAndCleanCondition(firstCond)
        myfirstWhileCond, myWhileCond, mysecondWhileCond = self.splitAndCleanCondition(secondCond)
        if ((myfirstIfCond == myfirstWhileCond)  and
            (myIfCond == myWhileCond) and
            (mysecondIfCond.isnumeric()) and
            (mysecondWhileCond.isalpha())):
            self.myTransformations.append(myTrans.C2V)
            return myTrans.I2W
        else:
            return myTrans.WhileNoIf
            
    def pythonFileFound(self):
        evalLine = self.line.rstrip()
        if ((evalLine.startswith("diff")) and (evalLine.endswith(".py"))):
            return True
        elif self.sameCommit() == False:
            return True
        else:
            return False
           

    def sameCommit(self):
        if self.line.find('green') > -1:   ## using the key word 'green' in the commit comment line to find the next commit 
            return False
        elif self.line == '':   ## looking for end of file
            return False
        else:
            return True
    
    def checkForDeletedNullValue(self):
        deletedNullValue = False
        if self.line.find("pass") > -1:
            deletedNullValue = True
        rtnMatchObj = re.search("return", self.line)
        if rtnMatchObj:
            deletedNullValue, rtnValue = self.returnWithNull()
        return deletedNullValue

    def checkForConstantOnReturn(self,line):
        return re.search(r'[0-9]+|[[]]|["]|[\\\']',line)   ## if return is followed by a number or [] or " or ', it is probably a constant
        
    def returnWithNull(self):
        rtnBoolean = False
        rtnValue = ''
        strLine = self.line.rstrip()
        splLine = strLine.split(" ")
        if len(splLine) > 1:
            rtnValue = splLine[len(splLine) - 1]
        if (len(splLine) == 1) or (rtnValue == 'None'): ## return with no value is basically Null
            rtnBoolean = True
        else:
            rtnBoolean = False
        return rtnBoolean, rtnValue

    def isTestFile(self, fileName):
        if fileName.startswith('test'):
            testFile = True
        else:
            testFile = False
        return testFile

    def extractFileName(self):
        strLine = self.line.rstrip() ## should be on diff line now
        splLine = strLine.split("/") ## split the line to get the file name, it's in the last element of the list
        fileName = splLine[len(splLine) - 1]
        return fileName

    def addNewFile(self, fileName, testFile):
        self.newFile = File.File(fileName, testFile, self.commits)
        self.myFiles.append(self.newFile)
        self.myTransformations.append(myTrans.NEWFILE)
        self.line = self.gitFile.readline() ## if this was a new file, then advance file pointer to index line
        fileIndex = len(self.myFiles) - 1
        return fileIndex


    def findExistingFileToAddCommitDetails(self, fileName):
        for x in self.myFiles:
            if x.extractFileName() == fileName:
                fileIndex = self.myFiles.index(x)
        
        return fileIndex


    def getCommits(self):
        return self.myCommits
    
    def getTransformations(self):
        return self.myTransformations
    
    def getFiles(self):
        return self.myFiles
    