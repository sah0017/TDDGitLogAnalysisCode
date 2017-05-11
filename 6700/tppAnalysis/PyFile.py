'''
Created on Jul 24, 2014

@author: susanha
'''
import PyFileCommitDetails
import Method
import re
import Commit
import GitFile
import DeletedLine
import TATestCase

class PyFile(object):
    '''
    classdocs
    '''
    @classmethod
    def pythonFileFound(self, line):
        evalLine = line.rstrip().lower()
        if ((evalLine.startswith("diff")) and (re.search(r"\b\py\b",evalLine))):
            if (re.search(r"\bprod\b", evalLine) or re.search(r"\btest\b",evalLine) or re.search(r"\bsoftwareprocess\b",evalLine)):
                if not (re.search(r"\b\__init__\b",evalLine)):
                    if not (re.search(r"\bmetadata\b",evalLine)):
                        return True
        elif Commit.Commit.foundNewCommit(evalLine) == True:
            return False
        return False

    @classmethod
    def extractFileName(self, line):
        strLine = line.rstrip() ## should be on diff line now
        splLine = strLine.split("/") ## split the line to get the file name, it's in the last element of the list
        path = splLine[len(splLine) - 2]
        fileName = splLine[len(splLine) - 1]
        return path, fileName

    def __init__(self, fileName, commitNbr):
        '''
        Constructor
        '''
        self.fileName = fileName
        self.nbrOfCommits = commitNbr
        self.commitDetails = []
        self.methods = []
        
    def setCommitDetails(self, assignmentName, commitNbr, addedLines, deletedLines, taTestLines, methodNames):
        myCommitDetails = PyFileCommitDetails.PyFileCommitDetails(assignmentName, commitNbr, addedLines, deletedLines, taTestLines, methodNames)
        self.commitDetails.append(myCommitDetails)

    def setMethodName(self, methodName):
        myMethod = Method.Method(methodName,[])
        self.methods.append(myMethod)
        
        
    def getCommitDetails(self):
        return self.commitDetails

    def analyzePyFile(self, path, assignmentName, gitFileHandle):
        self.myTransformations = []

        "Analyzes the information of an individual file within a commit"
        self.assignmentName = assignmentName
        fileAddedLines = 0
        fileDeletedLines = 0
        methods = []
        #notSBFile = self.isNotSandBoxOrBinaryFile(path, fileName)
        #if notSBFile:
        prodFile = self.isProdFile(path)
        line = GitFile.GitFile.readNextLine(gitFileHandle) ## either new file mode or index
        myTATestCase = TATestCase.TATestCase()
        self.TATestCaseDict = myTATestCase.retrieveTATestCaseObject()

        #if notSBFile:
        MypyFileCommitDetails = self.evaluateTransformationsInAFile(line, gitFileHandle)
        self.myFiles[fileIndex].setCommitDetails(assignmentName, commitNbr, fileAddedLines, fileDeletedLines, fileTATestLines, methods)
        return fileAddedLines, fileDeletedLines, fileTATestLines,  True

    def evaluateTransformationsInAFile(self, line, gitFileHandle):
        "Checks the line to see if it is a part of a transformation"
        addedLinesInFile = 0
        deletedLinesInFile = 0
        taTestLinesInFile = 0
        # deletedLinesArray = []
        # ifContents = []
        # whileContents = []
        currentMethod = Method.Method("Unknown", [])
        methodArray = []
        methodIndent = 0
        lineWithNoComments = ""

        while self.samePythonFile(gitFileHandle):             ## have we found a new python file within the same commit?
            prevLine = lineWithNoComments
            lineWithNoComments = self.removeComments(line, gitFileHandle)
            noLeadingPlus = lineWithNoComments[1:]
            noLeadingSpaces = noLeadingPlus.strip()
            currentIndent = len(noLeadingPlus) - len(noLeadingSpaces)
            if currentIndent <= methodIndent and len(noLeadingSpaces) > 0:
                currentMethod = Method.Method("Unknown", [])
                methodArray.append(currentMethod)
            if len(noLeadingSpaces) > 0:                 ## no need to go through all of this for a blank line
                if noLeadingSpaces.startswith("def "):   ## Looking for parameters in method call for assignment
                    methodLine = True
                    methodIndent = len(noLeadingPlus) - len(noLeadingSpaces)
                    currentMethod = self.getMethodNameAndParameters(noLeadingSpaces)
                    methodArray.append(currentMethod)
                else:
                    methodLine = False
                if (lineWithNoComments[0] == '-' and lineWithNoComments[1] != '-' and currentMethod.isATATestCase() == False):
                    #if prodFile:
                    deletedLine = self.processDeletedLine(lineWithNoComments)
                    currentMethod.addDeletedLine(deletedLine)

                if lineWithNoComments[0] == '+' and lineWithNoComments[1] != '+' and currentMethod.isATATestCase() == False:
                    #if prodFile:
                    currentMethod.addedLines = currentMethod.addedLines + 1
                    self.processAddedLine(currentMethod, methodIndent, lineWithNoComments,
                                          prevLine, noLeadingPlus, methodLine)

        for method in methodArray:
            addedLinesInFile = addedLinesInFile + method.getAddedLines()
            deletedLinesInFile = deletedLinesInFile + method.getDeletedLines()
            taTestLinesInFile = taTestLinesInFile + method.getTATestLines()
            #if method.getAddedLines() == 0 and method.getDeletedLines() == 0:
            #        methodArray.remove(method)      # empty method
        myPyFileDetails = PyFileCommitDetails.PyFileCommitDetails(self.assignmentName, self.nbrOfCommits,
                                                                  addedLinesInFile, deletedLinesInFile,
                                                                  taTestLinesInFile, methodArray)
        return myPyFileDetails


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
            if self.TATestCaseDict != None:
                if method.methodName in self.TATestCaseDict:       ## if they added one of the TA test cases, the number of lines in the test case will be removed from the number of test case lines that they wrote
                    method.updateTATestLines(self.TATestCaseDict[method.methodName])
                    method.setIsTATestCase(True)
        return method


    def processDeletedLine(self, lineWithNoComments):
        deletedLine = DeletedLine.DeletedLine(lineWithNoComments)
        deletedLine.deletedNullValue = self.checkForDeletedNullValue(lineWithNoComments)
        if re.search("return", lineWithNoComments):
            deletedLine.deletedReturn = True
            deletedLine.deletedLiteral = self.checkForConstantOnReturn(lineWithNoComments)
        if re.search(r"\bif .", lineWithNoComments):
            deletedLine.deletedIf = True
            ifConditionalParts = lineWithNoComments.split("if")
            ifConditional = ifConditionalParts[1].strip()
            deletedLine.deletedIfContents = ifConditional
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
                if not re.search("if __name__", prevLine):
                    methodLineNoLeadingSpaces = noLeadingPlus.strip()
                    methodLineIndent = len(noLeadingPlus) - len(methodLineNoLeadingSpaces)
                    if methodLineIndent > methodIndent:
                        self.myTransformations.append(self.myTrans.REC)
            #except Exception as inst:
            #    print self.fileName, type(inst)
        if re.search(r"\breturn\b", lineWithNoComments):
            self.processLineWithReturn(currentMethod, lineWithNoComments, noLeadingPlus)
        elif re.search(r"\bif.(?!_name__ == \"__main)", lineWithNoComments):
            self.myTransformations.append(self.myTrans.SF)
        elif re.search(r"\bwhile\b", lineWithNoComments):
            whileTrans = self.checkWhileForMatchingIfOrWhile(currentMethod, lineWithNoComments)
            self.myTransformations.append(whileTrans)
        elif re.search(r"\bfor\b", noLeadingPlus):
            self.myTransformations.append(self.myTrans.IT)
        elif re.search(r"\belif\b|\belse\b", noLeadingPlus):
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
        rtnBoolean, rtnValue = self.returnWithNull(lineWithNoComments)
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
        return DeletedLine.DeletedLine("")

    def stripGitActionAndSpaces(self, line):
        noPlus = line[1:]
        noPlus = noPlus.strip()
        return noPlus

    def removeComments(self, line, gitFileHandle):
        foundQuotedComment = True
        while foundQuotedComment:
            action = line[0]       # either blank space, + or -
            noPlus = self.stripGitActionAndSpaces(line)
            endCommentFound = False
            if noPlus.startswith("'''") or noPlus.startswith("\"\"\""):
                foundQuotedComment = True
                if len(noPlus) > 3 and noPlus.endswith("'''") or noPlus.endswith("\"\"\""):   #one-line comment
                    line = GitFile.GitFile.readNextLine(gitFileHandle)
                    if line == False:
                        line = ' '
                        foundQuotedComment = False
                    else:
                        endCommentFound = True
                while not endCommentFound:
                    line = GitFile.GitFile.readNextLine(gitFileHandle)
                    if line == False:
                        line = ' '
                        break
                    noPlus = self.stripGitActionAndSpaces(line)
                    if (line[0] == action) and (line[0] != " "):
                        if noPlus.startswith("'''") or noPlus.startswith("\"\"\"") or noPlus.endswith("'''") or noPlus.endswith("\"\"\""):
                            line = GitFile.GitFile.readNextLine(gitFileHandle)
                            if line == False:
                                line = ' '
                                foundQuotedComment = False
                            else:
                                endCommentFound = True
                    else:
                        endCommentFound = True
            else:
                foundQuotedComment = False
        if re.search(r"\#", self.line):
            noPlus = self.stripGitActionAndSpaces(line)
            if noPlus.startswith("#"):
                lineWithNoComments = "\r\n"
            else:
                commentSplit = line.split("#")
                lineWithNoComments = commentSplit[0]
        else:
            lineWithNoComments = line
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


    def samePythonFile(self, gitFileHandle):
        " Are we still in the same python file changes or is this a new python file? "
        line = GitFile.readNextLine(gitFileHandle)
        if line == False:              ## EOF
            line = ''
            return False
        evalLine = self.line.rstrip()
        if (evalLine.startswith("diff")):
            return False
        elif Commit.foundNewCommit(evalLine) == True:
            return False
        elif (re.search("if __name__", evalLine)):
            return False
        return True


    def checkForDeletedNullValue(self, line):
        deletedNullValue = False
        if line.find("pass") > -1:
            deletedNullValue = True
        rtnMatchObj = re.search("return", line)
        if rtnMatchObj:
            deletedNullValue = self.returnWithNull(line)
        return deletedNullValue

    def checkForConstantOnReturn(self,line):
        return re.search(r'[0-9]+|[[]]|["]|[\\\']',line)   ## if return is followed by a number or [] or " or ', it is probably a constant

    def returnWithNull(self, line):
        rtnBoolean = False
        rtnValue = ''
        strLine = line.rstrip()
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
        if (fileNameLower.startswith('prod')) or (fileNameLower.startswith('softwareprocess')):
            prodFile = True
        else:
            prodFile = False
        return prodFile
    '''
    def isNotSandBoxOrBinaryFile(self, path, fileName):
        pathLower = path.lower();
        if pathLower.startswith('sandbox'):
            notSBFile = False
        else:
            if (re.search(r"\b\pyc\b",fileName)):
                notSBFile = False
            elif (re.search(r"\b\__init__\b",fileName)):
                self.line = GitFile.readNextLine()
                notSBFile = False
            else:
                notSBFile = True
        return notSBFile
    '''

