'''
Created on Jul 10, 2014

@author: susanha
'''

# import subprocess
from Transformations import Trans 
import codecs
import Commit
import PyFile
import Assignment
import re
import os 
import Method
import jsonpickle
from DeletedLine import DeletedLine
from datetime import date
from time import strptime



class GitFile(object):
    " Analyzes a single git log file"

    myTrans = Trans()
    
    line = ''
    
    
    def __init__(self):
        '''
        Constructor
        '''
        self.fileName = ''
        self.currAssignment = 1
        self.myAssignmentsList = []
        self.myCommits = []
        self.myFiles = []
        self.gitFile = ''
        self.commits = 0
        self.myAssignment = Assignment.Assignment(1)
        self.myTransformations = []
        
    
    def analyzeGitLogFile(self, fileName):
        "Controls the looping through the git file"
        
        self.fileName = fileName
        self.gitFile = codecs.open(self.fileName)
        print self.fileName
       
        myAssignmentDict = Assignment.Assignment.get_assignment_dict()             # this dictionary tells us the dates for the asssignments
        self.currAssignmentDate = myAssignmentDict[self.currAssignment]     # last date for the first assignment
        self.readNextLine()                                                 # first line says commit
        for self.line in self.gitFile:
            if self.isCurrentAssignment():                                    # advances to next line to check the commit date
                self.commitType = self.getCommitType()                      # advances to next line to get commit type
                self.myAssignment.addCommitToAssignment(self.analyzeCommit(self.commitType))


            else:
                self.myAssignmentsList.append(self.myAssignment)
                self.currAssignment = self.currAssignment + 1
                self.myAssignment = Assignment.Assignment(self.currAssignment)
                
        self.myAssignmentsList.append(self.myAssignment)                # save last Assignment in the file to Assignments List
        #self.currAssignment = self.currAssignment + 1
        #self.myAssignment = Assignment.Assignment(self.currAssignment)
        self.gitFile.close()
        

    def getCommitType(self):
        self.readNextLine()             # advance to next line to get commit type
        commitType = self.line.strip()
        self.readNextLine()             # advance to next line to get the first file name in the commit
        return commitType


    def analyzeCommit(self,commitType):
        "Analyzes all the lines in an individual commit"
       
        self.myTransformations = []
        
        self.commits = self.commits + 1
        self.myNewCommit = Commit.Commit(self.commits)
        self.myNewCommit.set_commit_type(commitType)
        while self.foundNewCommit() == False:
            if self.pythonFileFound():
                path, fileName = self.extractFileName()
                addedLines, deletedLines, prodFile, notSBFile = self.analyzePyFile(path,fileName)
                if notSBFile:
                    
                    if prodFile:
                        self.myNewCommit.add_nbr_prod_files(1)
                        self.myNewCommit.add_added_lines_in_commit(addedLines)
                        self.myNewCommit.add_deleted_lines_in_commit(deletedLines)
                    else:
                        self.myNewCommit.add_nbr_test_files(1)
                        self.myNewCommit.add_added_test_loc(addedLines)
                        self.myNewCommit.add_deleted_test_loc(deletedLines)
                    
            else:
                self.line = self.readNextLine()
                if self.line == False:
                    self.line = ''
        nbrTrans = len(self.myTransformations)
        self.myNewCommit.add_number_of_transformations(nbrTrans)
        
        self.myNewCommit.set_transformations(self.myTransformations)
        
        return self.myNewCommit

    def analyzePyFile(self, path, fileName):
        "Analyzes the information of an individual file within a commit"
        fileAddedLines = 0
        fileDeletedLines = 0
        methods = []
        prodFile = False
        #notSBFile = self.isNotSandBoxOrBinaryFile(path, fileName)
        #if notSBFile:
        prodFile = self.isProdFile(path)
        self.line = self.gitFile.next() ## either new file mode or index
        self.fileIndex = self.findExistingFileToAddCommitDetails(fileName) 
        if (self.fileIndex == -1):
            self.fileIndex = self.addNewFile(fileName, prodFile)
        
        #if notSBFile:        
        fileAddedLines, fileDeletedLines, methods = self.evaluateTransformationsInAFile(prodFile)
        self.myFiles[self.fileIndex].setCommitDetails(self.commits, fileAddedLines, fileDeletedLines, methods)
        return fileAddedLines, fileDeletedLines, prodFile, True
    
    def evaluateTransformationsInAFile(self, prodFile):
        "Checks the line to see if it is a part of a transformation"
        addedLines = 0
        deletedLines = 0
        # deletedLinesArray = []
        # ifContents = []
        # whileContents = []
        currentMethod = Method.Method("Unknown",[])
        methodArray = []
        methodIndent = 0
        lineWithNoComments = ""
        

        while self.samePythonFile():             ## have we found a new python file within the same commit?
            prevLine = lineWithNoComments
            lineWithNoComments = self.removeComments()
            noLeadingPlus = lineWithNoComments[1:]
            noLeadingSpaces = noLeadingPlus.strip()
            currentIndent = len(noLeadingPlus) - len(noLeadingSpaces)
            if currentIndent <= methodIndent and len(noLeadingSpaces) > 0:
                currentMethod = Method.Method("Unknown",[])
                methodArray.append(currentMethod)
            if noLeadingPlus != "\r\n":                         ## no need to go through all of this for a blank line
                if noLeadingSpaces.startswith("def "):   ## Looking for parameters in method call for assignment
                    methodLine = True
                    methodIndent = len(noLeadingPlus) - len(noLeadingSpaces)
                    currentMethod = self.getMethodNameAndParameters(noLeadingSpaces)
                    methodArray.append(currentMethod)
                else:
                    methodLine = False
                if lineWithNoComments[0] == '-' and lineWithNoComments[1] != '-':
                    #if prodFile:
                    deletedLines = deletedLines + 1
                    deletedLine = self.processDeletedLine(lineWithNoComments)
                    currentMethod.addDeletedLine(deletedLine)
                
                if lineWithNoComments[0] == '+' and lineWithNoComments[1] != '+':
                    #if prodFile:
                    addedLines = addedLines + 1
                    currentMethod.addedLines = currentMethod.addedLines + 1
                    self.processAddedLine(currentMethod, methodIndent, lineWithNoComments, prevLine, noLeadingPlus, methodLine)
            
        for method in methodArray:
            if method.addedLines == 0:
                if len(method.deletedLines) == 0:
                    methodArray.remove(method)      # empty method
        return addedLines, deletedLines, methodArray

    def readNextLine(self):
        try:
            self.line = self.gitFile.next()
            return self.line
        except StopIteration as e:
            return False


    def getMethodNameAndParameters(self, lineWithNoLeadingSpaces):
        " Looks for method names and figures out what parameters are part of the method."
        defaultVal = False
        params = []
        methodData = lineWithNoLeadingSpaces.split(" ")   # def in methodData[0], method name in methodData[1] probably with (self, other params in methodData[2-n]
        if len(methodData) > 1:
            methodName = methodData[1].split("(")
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
            method = Method.Method(methodName[0], params)
        return method


    def processDeletedLine(self, lineWithNoComments):
        deletedLine = DeletedLine(lineWithNoComments)
        deletedLine.deletedNullValue = self.checkForDeletedNullValue()
        if re.search("return", lineWithNoComments):
            deletedLine.deletedReturn = True
            deletedLine.deletedLiteral = self.checkForConstantOnReturn(lineWithNoComments)
        if re.search(r"\bif .", lineWithNoComments):
            deletedLine.deletedIf = True
            ifConditionalParts = lineWithNoComments.split("if")
            ifConditional = ifConditionalParts[1].strip()
            deletedLine.deletedIfContents=ifConditional
        if re.search(r"\bwhile .", lineWithNoComments):
            deletedLine.deletedWhile = True
            whileConditionalParts = lineWithNoComments.split("while")
            whileConditional = whileConditionalParts[1].strip()
            deletedLine.deletedWhileContents = whileConditional
        return deletedLine




    def processAddedLine(self, currentMethod, methodIndent, lineWithNoComments, prevLine, noLeadingPlus, methodLine):
        if re.search(r"\bpass\b", lineWithNoComments):      # Transformation 1
            self.myTransformations.append(self.myTrans.NULL)
        if currentMethod.methodName != "Unknown" and not methodLine:             # Transformation 9
            myRecurseSearchString = r"\b(?=\w){0}\b(?!\w)\(\)".format(currentMethod.methodName)
            #try:
            if re.search(myRecurseSearchString, lineWithNoComments):
                if not (re.search("if __name__", prevLine)):
                    methodLineNoLeadingSpaces = noLeadingPlus.strip()
                    methodLineIndent = len(noLeadingPlus) - len(methodLineNoLeadingSpaces)
                    if methodLineIndent > methodIndent:
                        self.myTransformations.append(self.myTrans.REC)
            #except Exception as inst:
            #    print self.fileName, type(inst)
        if re.search(r"\breturn\b", lineWithNoComments):
            self.processLineWithReturn(currentMethod, lineWithNoComments, noLeadingPlus)
        elif (re.search(r"\bif.(?!_name__ == \"__main)", lineWithNoComments)):
            self.myTransformations.append(self.myTrans.SF)
        elif (re.search(r"\bwhile\b", lineWithNoComments)):
            whileTrans = self.checkWhileForMatchingIfOrWhile(currentMethod, lineWithNoComments)
            self.myTransformations.append(whileTrans)
        elif (re.search(r"\bfor\b", noLeadingPlus)):
            self.myTransformations.append(self.myTrans.IT)
        elif (re.search(r"\belif\b|\belse\b", noLeadingPlus)):
            self.myTransformations.append(self.myTrans.ACase)
        elif re.search(r"[+/*%\-]|\bmath.\b", noLeadingPlus):
            #elif (re.search(r"=",noLeadingPlus)):
            self.myTransformations.append(self.myTrans.AComp)
        #    if not (re.search(r"['\"]",noLeadingPlus)):       ## Not Add Computation if the character is inside a quoted string
        #        if not (re.search(r"==",noLeadingPlus)):      ## evaluation, not assignment
        assignmentVars = noLeadingPlus.split("=")               # Check to see if we are assigning a new value to an input parameter
        if len(assignmentVars) > 1:
            assignmentVar = assignmentVars[0].strip()
            for x in currentMethod.parameters:
                if x == assignmentVar:
                    self.myTransformations.append(self.myTrans.AS)

    def processLineWithReturn(self, currentMethod, lineWithNoComments, noLeadingPlus):
        rtnBoolean, rtnValue = self.returnWithNull()
        deletedLine = self.checkDeletedLinesForReturn(currentMethod)
        if rtnBoolean == True: # Transformation 1
            self.myTransformations.append(self.myTrans.NULL) ## this is either a 'return' or a 'return None'
        elif self.checkForConstantOnReturn(rtnValue): ## if there are constants and
            if deletedLine.deletedNullValue == True: ## if there was a Null expression before, they probably did Transformation 2 Null to Constant
                self.myTransformations.append(self.myTrans.N2C)
            else:
                self.myTransformations.append(self.myTrans.ConstOnly) ## if constants but no previous Null, they probably just went straight to constant
        elif deletedLine.deletedLiteral: ## and the delete section removed a 'return' with a constant
            self.myTransformations.append(self.myTrans.C2V) ## then it is probably a Transformation 3 constant to variable
        elif re.search(r"[+/*%\-]|\bmath.\b", noLeadingPlus):   # if they're doing math or some math function, it is a Transformation 4 Add Computation.
            self.myTransformations.append(self.myTrans.AComp)
        else:   
            self.myTransformations.append(self.myTrans.VarOnly) ##  if we got to this point, they went straight to a variable.
        for parm in currentMethod.parameters:
            if rtnValue == parm: ## if the return value is a parameter, then it is a Transformation 11 assign.
                self.myTransformations.append(self.myTrans.AS)

        ## if it wasn't constants on the return
        ## this looks for constants after 'return'
    def checkDeletedLinesForReturn(self, currentMethod):
        for dLine in currentMethod.deletedLines:
            if dLine.deletedReturn:
                return dLine
        return DeletedLine("")    
        

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
                    self.line = self.gitFile.next()
                    endCommentFound = True
                while not endCommentFound:
                    self.line = self.readNextLine()
                    if self.line == False:
                        self.line = ' '
                        break
                    noPlus = self.stripGitActionAndSpaces()
                    if (self.line[0] == action) and (self.line[0] != " "):
                        if noPlus.startswith("'''") or noPlus.startswith("\"\"\"") or noPlus.endswith("'''") or noPlus.endswith("\"\"\""):
                            self.line = self.gitFile.next()
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

    def checkWhileForMatchingIfOrWhile(self, currentMethod, currentLine):
        whileConditionalParts = currentLine.split("while")
        whileCondition = whileConditionalParts[1].strip()
        whileTrans = self.myTrans.WhileNoIf
        for dLine in currentMethod.deletedLines:
            if dLine.deletedIf:
                if whileCondition == dLine.deletedIfContents:
                    return self.myTrans.I2W
                else:
                    whileTrans = self.myTrans.WhileNoIf
            if dLine.deletedWhile:
                whileTrans = self.checkForConstantToVariableInCondition(dLine.deletedWhileContents,whileCondition)
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
                (mysecondIfCond.isdigit()) and
                (mysecondWhileCond.isalpha())):
                self.myTransformations.append(self.myTrans.C2V)
                return self.myTrans.I2W
        return self.myTrans.WhileNoIf
            
    def pythonFileFound(self):
        evalLine = self.line.rstrip()
        if ((evalLine.startswith("diff")) and (re.search(r"\b\py\b",evalLine))):
            if re.search(r"\bprod\b", evalLine) or re.search(r"\btest\b",evalLine):
                if not (re.search(r"\b\__init__\b",evalLine)):
                    return True
        elif self.foundNewCommit() == True:
            return False
        return False
        
    def samePythonFile(self):
        " Are we still in the same python file changes or is this a new python file? "
        self.line = self.readNextLine()
        if self.line == False:              ## EOF
            self.line = ''
            return False
        evalLine = self.line.rstrip()
        if (evalLine.startswith("diff")):
            return False
        elif self.foundNewCommit() == True:
            return False
        elif (re.search("if __name__", evalLine)):
            return False
        return True

    def foundNewCommit(self):
        " Are we still in the same commit or is this a new one? "
        if self.line.startswith("\"commit"):   ## using this key word in the commit comment line to find the next commit 
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
            deletedNullValue = self.returnWithNull()
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

    def isCurrentAssignment(self):
        " a git file can contain multiple assignments.  This is looking for the current one for analysis."
        #self.line = self.readNextLine()         # line after commit contains the commit date
        dateLine = self.line.split(" ")
        commitMonth = strptime(dateLine[1], '%b').tm_mon
        commitDay = int(dateLine[2])
        commitYear = int(dateLine[4])
        commitDate = date(commitYear,commitMonth,commitDay)
        
        
        if (commitDate <= self.currAssignmentDate):
            return True
        else:
            return False

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
                self.line = self.gitFile.next()
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
        " This is a new file that isn't in our analysis yet. "
        self.newFile = PyFile.PyFile(fileName, prodFile, self.commits)
        self.myFiles.append(self.newFile)
        self.myTransformations.append(self.myTrans.NEWFILE)
        self.line = self.gitFile.next() ## if this was a new file, then advance file pointer to index line
        fileIndex = len(self.myFiles) - 1
        return fileIndex


    def findExistingFileToAddCommitDetails(self, fileName):
        fileIndex = -1
        for x in self.myFiles:
            if x.extractFileName() == fileName:
                fileIndex = self.myFiles.index(x)
        
        return fileIndex


    def getFileName(self):
        return self.fileName
    
    def getAssignments(self):
        return self.myAssignmentsList

    def setAssignments(self,assignmentList):
        self.myAssignmentsList = assignmentList
    
    def getCommits(self):
        return self.myCommits
    
    def get_transformations(self):
        return self.myTransformations
    
    def getFiles(self):
        return self.myFiles
    
    def storeGitReportObject(self, fileName):
        out_s = open(fileName+'.json', 'w')

        # Write to the stream
        myJsonString = jsonpickle.encode(self)
        out_s.write(myJsonString)
        out_s.close()
            
    def retrieveGitReportObject(self,filename):
        
        in_s = open(filename+'.json', 'r')
        
        # Read from the stream
        myJsonString = in_s.read()
        try:
            gitReportObject = jsonpickle.decode(myJsonString)
        except Exception as e:
            gitReportObject = None
        
        in_s.close()
        
        return gitReportObject
    