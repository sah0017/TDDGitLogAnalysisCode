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
import Method

myTrans = Transformations.Trans() 

class GitFile(object):
    " Analyzes a single git log file"
 
    line = ''
    
    def __init__(self, fileName, assignment):
        '''
        Constructor
        '''
        self.fileName = fileName
        self.assignment = assignment
        self.myCommits = []
        self.myFiles = []
        self.gitFile = ''
        self.commits = 0

    def readGitFile(self):
        "Controls the looping through the git file"
        
        self.gitFile = codecs.open(self.fileName, encoding='utf-8')
        print self.fileName
        
        for x in range(0, 39):                      ##  we don't need the first 40 lines of file
            self.line = self.gitFile.readline() 

        for self.line in self.gitFile:
            # print self.line
            if self.pythonFileFound(self.assignment):
                self.analyzeCommit()
 
        self.gitFile.close()


    def currentAssignment(self):
        searchResult = re.search(self.assignment, self.line)
        if (searchResult==None):
            return False
        else:
            if (self.line.startswith("diff")):
                return True

    def analyzeCommit(self):
        "Analyzes all the lines in an individual commit"
        commitProdAddedLines = 0
        commitProdDeletedLines = 0
        commitTestAddedLines = 0
        commitTestDeletedLines = 0
        
        testFiles = 0
        prodFiles = 0
        nbrTrans = 0
        self.myTransformations = []
        while (self.currentAssignment() == False):
            self.line = self.gitFile.readline()
            if self.foundNewCommit():   ## This is the correct assignment
                return
        if (self.currentAssignment() == True):
            self.commits = self.commits + 1
            while self.foundNewCommit() == False:
                path, fileName = self.extractFileName()
                if self.pythonFileFound(self.assignment):
                    addedLines, deletedLines, prodFile, notSBFile = self.analyzeFile(path,fileName)
                    if notSBFile:
                        
                        if prodFile:
                            prodFiles = prodFiles + 1
                            commitProdAddedLines = commitProdAddedLines + addedLines
                            commitProdDeletedLines = commitProdDeletedLines + deletedLines
                        else:
                            testFiles = testFiles + 1
                            commitTestAddedLines = commitTestAddedLines + addedLines
                            commitTestDeletedLines = commitTestDeletedLines + deletedLines
                        
                else:
                    self.line = self.gitFile.readline()
            nbrTrans = len(self.myTransformations)
            self.newCommit = Commit.Commit(self.commits, commitProdAddedLines,commitProdDeletedLines, commitTestAddedLines,
                                           commitTestDeletedLines, testFiles, prodFiles, nbrTrans)
            for trans in self.myTransformations:
                self.newCommit.addTransformation(trans)
            self.myCommits.append(self.newCommit)
   
    def analyzeFile(self, path, fileName):
        "Analyzes the information of an individual file in a commit"
        fileAddedLines = 0
        fileDeletedLines = 0
        methodNames = []
        prodFile = False
        #notSBFile = self.isNotSandBoxOrBinaryFile(path, fileName)
        #if notSBFile:
        prodFile = self.isProdFile(path)
        self.line = self.gitFile.readline() ## either new file mode or index
        self.fileIndex = self.findExistingFileToAddCommitDetails(fileName) 
        if (self.fileIndex == -1):
            self.fileIndex = self.addNewFile(fileName, prodFile)
        '''        
        for x in range(0, 2): ## skips --- line, +++ line
            if self.pythonFileFound(self.assignment):
                break
            self.line = self.gitFile.readline()
        '''
        #if notSBFile:        
        fileAddedLines, fileDeletedLines, methodNames = self.evaluateTransformations(prodFile)
        self.myFiles[self.fileIndex].setCommitDetails(self.commits, fileAddedLines, fileDeletedLines, methodNames)
        return fileAddedLines, fileDeletedLines, prodFile, True
    




    def getMethodNameAndParameters(self, methodName, methodNames, defaultVal, params, noLeadingSpaces):
        methodData = noLeadingSpaces.split(" ")
        if len(methodData) > 1:
            methodName = methodData[1].split("(")
            methodNames.append(methodName[0])
            params = methodData[2:]
            if len(params) > 0:
                x = 0
                for parm in params:
                    noDefaultVal = parm.split("=")
                    if len(noDefaultVal) > 1:
                        params[x] = noDefaultVal[0]
                        defaultVal = True
                    x = x + 1
                
                if not defaultVal:
                    lastParam = params[len(params) - 1]
                    lastParam = lastParam[0:len(lastParam) - 2] ## removes ): from last parameter
                    params[len(params) - 1] = lastParam
                defaultVal = False
                #print params
        return methodName, params

    def evaluateTransformations(self, prodFile):
        "Checks the line to see if it is a part of a transformation"
        addedLines = 0
        deletedLines = 0
        deletedNullValue = False
        deletedLiteral = False
        deletedIf = False
        deletedWhile = False
        ifContents = []
        whileContents = []
        methodName = ""
        methodNames = []
        methodIndent = 0
        lineWithNoComments = ""
        defaultVal = False
        params = []
        while self.samePythonFile():             ## have we found a new python file within the same commit?
            prevLine = lineWithNoComments
            lineWithNoComments = self.removeComments()
            noLeadingPlus = lineWithNoComments[1:]
            noLeadingSpaces = noLeadingPlus.strip()
            currentIndent = len(noLeadingPlus) - len(noLeadingSpaces)
            if currentIndent <= methodIndent:
                methodName=""
            if noLeadingPlus != "\r\n":                         ## no need to go through all of this for a blank line
                if noLeadingSpaces.startswith("def"):   ## Looking for parameters in method call for assignment
                    methodLine = True
                    methodIndent = len(noLeadingPlus) - len(noLeadingSpaces)
                    methodName, params = self.getMethodNameAndParameters(methodName, methodNames, defaultVal, params, noLeadingSpaces)
                else:
                    methodLine = False
                if lineWithNoComments[0] == '-' and lineWithNoComments[1] != '-':
                    deletedLines = deletedLines + 1
                    if prodFile:
                        deletedNullValue = self.checkForDeletedNullValue()
                        if re.search("return", lineWithNoComments):
                            deletedLiteral = self.checkForConstantOnReturn(lineWithNoComments)
                        if re.search(r"\bif .", lineWithNoComments):
                            deletedIf = True
                            ifConditionalParts = lineWithNoComments.split("if")
                            ifConditional = ifConditionalParts[1].strip()
                            ifContents.append(ifConditional)
                        if re.search(r"\bwhile .", lineWithNoComments):
                            deletedWhile = True
                            whileConditionalParts = lineWithNoComments.split("while")
                            whileConditional = whileConditionalParts[1].strip()
                            whileContents.append(whileConditional)
                    
                if lineWithNoComments[0] == '+' and lineWithNoComments[1] != '+':
                    addedLines = addedLines + 1
                    if prodFile:
                        if re.search(r"\bpass\b",lineWithNoComments):
                            self.myTransformations.append(myTrans.NULL)
                        if methodName != "" and not methodLine:
                            myRecurseSearchString = r"\b(?=\w){0}\b(?!\w)\(\)".format(methodName[0])
                            #try:
                            if re.search(myRecurseSearchString, lineWithNoComments):
                                if not (re.search("if __name__ == '__main__':",prevLine)):
                                    methodLineNoLeadingSpaces = noLeadingPlus.strip()
                                    methodLineIndent = len(noLeadingPlus) - len(methodLineNoLeadingSpaces)
                                    if methodLineIndent > methodIndent:
                                        self.myTransformations.append(myTrans.REC)
                            #except Exception as inst:
                            #    print self.fileName, type(inst)
                        if re.search(r"\breturn\b", lineWithNoComments):
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
                                    else:
                                        if re.search(r"[+/*%\-]|\bmath.\b",noLeadingPlus):
                                            self.myTransformations.append(myTrans.AComp)
                                        for parm in params:
                                            if rtnValue == parm:                ## if the return value is a parameter, then it is an assign.
                                                self.myTransformations.append(myTrans.AS)
                                        self.myTransformations.append(myTrans.VarOnly)  ##  if we got to this point, they went straight to a variable.
                        elif (re.search(r"\bif.(?!_name__ == \"__main)",lineWithNoComments)):
                            self.myTransformations.append(myTrans.SF)
                        elif (re.search(r"\bwhile\b",lineWithNoComments)):
                            whileTrans = self.checkWhileForMatchingIfOrWhile(deletedIf, ifContents, deletedWhile, whileContents)
                            self.myTransformations.append(whileTrans)              
                        elif (re.search(r"\bfor\b",noLeadingPlus)):
                            self.myTransformations.append(myTrans.IT)
                        elif (re.search(r"\belif\b|\belse\b",noLeadingPlus)):
                            self.myTransformations.append(myTrans.ACase)
                       # elif (re.search(r"=",noLeadingPlus)):
                       #     if not (re.search(r"['\"]",noLeadingPlus)):       ## Not Add Computation if the character is inside a quoted string
                       #         if not (re.search(r"==",noLeadingPlus)):      ## evaluation, not assignment
                        elif re.search(r"[+/*%\-]|\bmath.\b",noLeadingPlus):
                            self.myTransformations.append(myTrans.AComp)
                        assignmentVars = noLeadingPlus.split("=")
                        assignmentVar = assignmentVars[0].strip()
                        for x in params:
                            if x == assignmentVar:
                                self.myTransformations.append(myTrans.AS)
            self.line = self.gitFile.readline()
        
        return addedLines, deletedLines, methodNames

    def stripGitActionAndSpaces(self):
        noPlus = self.line[1:]
        noPlus = noPlus.strip()
        return noPlus

    def removeComments(self):
        foundQuotedComment = True
        while foundQuotedComment:
            action = self.line[0]       # either blank space, + or -
            noPlus = self.stripGitActionAndSpaces()
            endCommentFound = False
            if noPlus.startswith("'''") or noPlus.startswith("\"\"\""):
                foundQuotedComment = True
                if len(noPlus) > 3 and noPlus.endswith("'''") or noPlus.endswith("\"\"\""):   #one-line comment
                    self.line = self.gitFile.readline()
                    endCommentFound = True
                while not endCommentFound:
                    self.line = self.gitFile.readline()
                    noPlus = self.stripGitActionAndSpaces()
                    if (self.line[0] == action) and (self.line[0] != " "):
                        if noPlus.startswith("'''") or noPlus.startswith("\"\"\"") or noPlus.endswith("'''") or noPlus.endswith("\"\"\""):
                            self.line = self.gitFile.readline()
                            endCommentFound = True
                    else:
                        endCommentFound = True
            else:
                foundQuotedComment = False
        if re.search(r"\#", self.line):
            noPlus = self.stripGitActionAndSpaces()
            if noPlus.startswith("#"):
                lineWithNoComments = "\r\n"
            else:
                commentSplit = self.line.split("#")
                lineWithNoComments = commentSplit[0]
        else:
            lineWithNoComments = self.line
        return lineWithNoComments

    def checkWhileForMatchingIfOrWhile(self, deletedIf, ifContents, deletedWhile, delWhileContents):
        whileConditionalParts = self.line.split("while")
        whileCondition = whileConditionalParts[1].strip()
        whileTrans = myTrans.WhileNoIf
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
        if len(mySplit) == 3:
            myfirstcond = mySplit[0]
            mycond = mySplit[1]
            mysecondcond = mySplit[2]
            if myfirstcond.startswith("("):
                myfirstcond = myfirstcond[1:]
            removeTrailingChars = re.search(r"[a-zA-Z0-9_^):]",mysecondcond)
            if removeTrailingChars:
                mysecondcond = removeTrailingChars.group(0)
            return myfirstcond, mycond, mysecondcond
        else:
            return None, None, None

    def checkForConstantToVariableInCondition(self, firstCond, secondCond):
        myfirstIfCond, myIfCond, mysecondIfCond = self.splitAndCleanCondition(firstCond)
        myfirstWhileCond, myWhileCond, mysecondWhileCond = self.splitAndCleanCondition(secondCond)
        if myfirstIfCond != None:
            if ((myfirstIfCond == myfirstWhileCond)  and
                (myIfCond == myWhileCond) and
                (mysecondIfCond.isnumeric()) and
                (mysecondWhileCond.isalpha())):
                self.myTransformations.append(myTrans.C2V)
                return myTrans.I2W
        return myTrans.WhileNoIf
            
    def pythonFileFound(self, assignment):
        evalLine = self.line.rstrip()
        if ((evalLine.startswith("diff")) and (re.search(r"\b\py\b",evalLine))):
            if (re.search(assignment,evalLine)):
                
            #print evalLine
                if re.search(r"\bprod\b", evalLine) or re.search(r"\btest\b",evalLine):
                    if not (re.search(r"\b\__init__\b",evalLine)):
                        return True
        elif self.foundNewCommit() == True:
            return True
        return False
        
    def samePythonFile(self):
        evalLine = self.line.rstrip()
        if (evalLine.startswith("diff")):
            return False
        elif self.foundNewCommit() == True:
            return False
        return True

    def foundNewCommit(self):
        if self.line.find('Signed-off-by') > -1:   ## using this key word in the commit comment line to find the next commit 
            return True
        elif self.line == '':   ## looking for end of file
            return True
        else:
            return False
    
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

    def isProdFile(self, fileName):
        fileNameLower = fileName.lower();
        if fileNameLower.startswith('prod'):
            prodFile = True
        else:
            prodFile = False
        return prodFile

    def isNotSandBoxOrBinaryFile(self, path, fileName):
        pathLower = path.lower();
        if pathLower.startswith('sandbox'):
            notSBFile = False
        else:
            if (re.search(r"\b\pyc\b",fileName)):
                notSBFile = False
            elif (re.search(r"\b\__init__\b",fileName)):
                self.line = self.gitFile.readline()
                notSBFile = False
            else:
                notSBFile = True
        return notSBFile

    def extractFileName(self):
        strLine = self.line.rstrip() ## should be on diff line now
        splLine = strLine.split("/") ## split the line to get the file name, it's in the last element of the list
        path = splLine[len(splLine) - 2]
        fileName = splLine[len(splLine) - 1]
        return path, fileName

    def addNewFile(self, fileName, prodFile):
        self.newFile = File.File(fileName, prodFile, self.commits)
        self.myFiles.append(self.newFile)
        self.myTransformations.append(myTrans.NEWFILE)
        self.line = self.gitFile.readline() ## if this was a new file, then advance file pointer to index line
        fileIndex = len(self.myFiles) - 1
        return fileIndex


    def findExistingFileToAddCommitDetails(self, fileName):
        fileIndex = -1
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

    