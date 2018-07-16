'''
Created on Jul 24, 2014

@author: susanha

Used by:
At a class level, determines if a new python file has been found in the git log, and also extracts the python
file name.
Parameters:  when instantiated, receives a path, a file name, and a commit number.
Results:  Contain the code that analyzes the TPP transformations in the commit.
Uses:  Commit

'''
import PyFileCommitDetails
import Method
import re
import Commit
import GitFile
import DeletedLine
import Transformations


class PyFile(object):
    '''
    classdocs
    '''

    #myTrans = Trans()   # get Transformation static variables and dictionary from Transformation class

    @classmethod
    def pythonFileFound(self, line):
        evalLine = line.rstrip().lower()
        if (evalLine.startswith("diff")) and (re.search(r"\b\py\b",evalLine)):
            if (re.search(r"\bprod\b", evalLine) or re.search(r"\btest\b",evalLine)
                    or re.search(r"\bsoftwareprocess\b",evalLine) or re.search(r"\brcube\b",evalLine)):
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

    def __init__(self, path, fileName, commitNbr):
        '''
        Constructor
        '''
        self.fileName = fileName
        self.commitNbr = commitNbr  # this is the commit when it was created
        self.prodFile = self.isProdOrTest(path, fileName)
        self.commitDetails = []   # a list of pyFileCommitDetail objects on this file in this commit
        self.methods = []         # a list of Method objects in this pyFile
        self.transformations = []

    def analyzePyFile(self, gitfile_handle):
        "Analyzes the information of an individual file within a commit"
        gitfile_handle.readNextLine() ## either new file mode or index

        my_pyfile_commit_details = self.evaluateTransformationsInAFile(gitfile_handle)
        self.setCommitDetails(my_pyfile_commit_details)
        return my_pyfile_commit_details

    def evaluateTransformationsInAFile(self, gitfile_handle):
        "Checks the line to see if it is a part of a transformation"
        added_lines_in_file = 0
        deleted_lines_in_file = 0
        ta_test_lines_in_file = 0
        # deletedLinesArray = []
        # ifContents = []
        # whileContents = []
        current_method = Method.Method("Unknown", [])
        method_array = []
        method_indent = 0
        line_with_no_comments = ""

        line = gitfile_handle.readNextLine()

        while self.samePythonFile(line):             ## have we found a new python file within the same commit?
            prev_line = line_with_no_comments
            line_with_no_comments = self.removeComments(gitfile_handle)
            no_leading_plus = line_with_no_comments[1:]
            no_leading_spaces = no_leading_plus.strip()
            current_indent = len(no_leading_plus) - len(no_leading_spaces)
            if current_indent <= method_indent and len(no_leading_spaces) > 0:
                current_method = Method.Method("Unknown", [])
                method_array.append(current_method)
            if len(no_leading_spaces) > 0:                 ## no need to go through all of this for a blank line
                if no_leading_spaces.startswith("def "):   ## Looking for parameters in method call for assignment
                    method_line = True
                    method_indent = len(no_leading_plus) - len(no_leading_spaces)
                    current_method = self.getMethodNameAndParameters(no_leading_spaces)
                    method_array.append(current_method)
                elif line_with_no_comments[0] == "@":   # tells us what class/method the changes are from
                    if re.search("def ", no_leading_spaces):
                        method_name_parts = no_leading_spaces.split("def ")
                        method_name = method_name_parts[1].split("(")
                        current_method.setMethodName(method_name[0])
                        method_array.append(current_method)
                else:
                    method_line = False
                if line_with_no_comments[0] == '-' and line_with_no_comments[1] != '-' and current_method.isATATestCase() is False:
                    #if prodFile:
                    deleted_line = self.processDeletedLine(line_with_no_comments)
                    current_method.addDeletedLine(deleted_line)

                if line_with_no_comments[0] == '+' and line_with_no_comments[1] != '+' and current_method.isATATestCase() is False:
                    #if prodFile:
                    current_method.addedLines = current_method.addedLines + 1
                    self.processAddedLine(current_method, method_indent, line_with_no_comments,
                                          prev_line, no_leading_plus, method_line)
            line = gitfile_handle.readNextLine()

        for method in method_array:
            added_lines_in_file = added_lines_in_file + method.getAddedLines()
            deleted_lines_in_file = deleted_lines_in_file + method.getDeletedLines()
            ta_test_lines_in_file = ta_test_lines_in_file + method.getTATestLines()
            #if method.getAddedLines() == 0 and method.getDeletedLines() == 0:
            #        method_array.remove(method)      # empty method
        my_py_file_details = PyFileCommitDetails.PyFileCommitDetails(self.commitNbr,
                                                                     added_lines_in_file, deleted_lines_in_file,
                                                                     ta_test_lines_in_file, method_array)
        return my_py_file_details


    def getMethodNameAndParameters(self, line_with_no_leading_spaces):
        " Looks for method names and figures out what parameters are part of the method."
        default_val = False
        params = []
        method_data = line_with_no_leading_spaces.split(" ")   # def in method_data[0], method name in method_data[1] probably with (self, other params in method_data[2-n]
        if len(method_data) > 1:
            method_name = method_data[1].split("(")
            params = method_data[2:]
            if len(params) > 0:
                x = 0
                for parm in params:
                    no_default_val = parm.split("=")
                    if len(no_default_val) > 1:
                        params[x] = no_default_val[0]
                        default_val = True
                    x = x + 1

                if not default_val:
                    last_param = params[len(params) - 1]
                    last_param = last_param[0:len(last_param) - 2] ## removes ): from last parameter
                    params[len(params) - 1] = last_param
                default_val = False
                #print params
            method = Method.Method(method_name[0], params)
            if GitFile.GitFile.TATestCaseDict is not None:
                if method.methodName in GitFile.GitFile.TATestCaseDict:       ## if they added one of the TA test cases, the number of lines in the test case will be removed from the number of test case lines that they wrote
                    method.updateTATestLines(GitFile.GitFile.TATestCaseDict[method.methodName])
                    method.setIsTATestCase(True)
        return method

    def processDeletedLine(self, line_with_no_comments):
        deleted_line = DeletedLine.DeletedLine(line_with_no_comments)
        deleted_line.deletedNullValue = self.checkForDeletedNullValue(line_with_no_comments)
        if re.search("return", line_with_no_comments):
            deleted_line.deletedReturn = True
            deleted_line.deletedLiteral = self.checkForConstantOnReturn(line_with_no_comments)
        if re.search(r"\bif .", line_with_no_comments):
            deleted_line.deletedIf = True
            ifConditionalParts = line_with_no_comments.split("if")
            ifConditional = ifConditionalParts[1].strip()
            deleted_line.deletedIfContents = ifConditional
        if re.search(r"\bwhile .", line_with_no_comments):
            deleted_line.deletedWhile = True
            whileConditionalParts = line_with_no_comments.split("while")
            whileConditional = whileConditionalParts[1].strip()
            deleted_line.deletedWhileContents = whileConditional
        return deleted_line

    def processAddedLine(self, current_method, method_indent, line_with_no_comments, prev_line, no_leading_plus, method_line):
        if re.search(r"\bpass\b", line_with_no_comments):      # Transformation 1
            self.addToTransformationList(Transformations.Trans.getTransValue("NULL"))
        if current_method.methodName != "Unknown" and not method_line:             # Transformation 9
            myRecurseSearchString = r"\b(?=\w){0}\b(?!\w)\(\)".format(current_method.methodName)
            try:
                if re.search(myRecurseSearchString, line_with_no_comments):
                    if not re.search("if __name__", prev_line):
                        methodLineNoLeadingSpaces = no_leading_plus.strip()
                        methodLineIndent = len(no_leading_plus) - len(methodLineNoLeadingSpaces)
                        if methodLineIndent > method_indent:
                            self.addToTransformationList(Transformations.Trans.getTransValue("REC"))
            except Exception as inst:
                print self.fileName, myRecurseSearchString, line_with_no_comments, type(inst)
        if re.search(r"\breturn\b", line_with_no_comments):
            self.processLineWithReturn(current_method, line_with_no_comments, no_leading_plus)
        elif re.search(r"\bif.(?!_name__ == \"__main)", line_with_no_comments):
            self.addToTransformationList(Transformations.Trans.getTransValue("SF"))
        elif re.search(r"\bwhile\b", line_with_no_comments):
            whileTrans = self.checkWhileForMatchingIfOrWhile(current_method, line_with_no_comments)
            self.addToTransformationList(whileTrans)
        elif re.search(r"\bfor\b", no_leading_plus):
            self.addToTransformationList(Transformations.Trans.getTransValue("IT"))
        elif re.search(r"\belif\b|\belse\b", no_leading_plus):
            self.addToTransformationList(Transformations.Trans.getTransValue("ACase"))
        elif re.search(r"[+/*%\-]|\bmath.\b", no_leading_plus):
            #elif (re.search(r"=",noLeadingPlus)):
            self.addToTransformationList(Transformations.Trans.getTransValue("AComp"))
        #    if not (re.search(r"['\"]",noLeadingPlus)):       ## Not Add Computation if the character is inside a quoted string
        #        if not (re.search(r"==",noLeadingPlus)):      ## evaluation, not assignment
        assignmentVars = no_leading_plus.split("=")               # Check to see if we are assigning a new value to an input parameter
        if len(assignmentVars) > 1:
            assignmentVar = assignmentVars[0].strip()
            for x in current_method.parameters:
                if x == assignmentVar:
                    self.addToTransformationList(Transformations.Trans.getTransValue("AS"))

    def processLineWithReturn(self, current_method, line_with_no_comments, no_leading_plus):
        rtnBoolean, rtnValue = self.returnWithNull(line_with_no_comments)
        deletedLine = self.checkDeletedLinesForReturn(current_method)
        if rtnBoolean == True: # Transformation 1
            self.addToTransformationList(Transformations.Trans.getTransValue("NULL")) ## this is either a 'return' or a 'return None'
        elif self.checkForConstantOnReturn(rtnValue): ## if there are constants and
            if deletedLine.deletedNullValue == True: ## if there was a Null expression before, they probably did Transformation 2 Null to Constant
                self.addToTransformationList(Transformations.Trans.getTransValue("N2C"))
            else:
                self.addToTransformationList(Transformations.Trans.getTransValue("ConstOnly")) ## if constants but no previous Null, they probably just went straight to constant
        elif deletedLine.deletedLiteral: ## and the delete section removed a 'return' with a constant
            self.addToTransformationList(Transformations.Trans.getTransValue("C2V")) ## then it is probably a Transformation 3 constant to variable
        elif re.search(r"[+/*%\-]|\bmath.\b", no_leading_plus):   # if they're doing math or some math function, it is a Transformation 4 Add Computation.
            self.addToTransformationList(Transformations.Trans.getTransValue("AComp"))
        else:
            self.addToTransformationList(Transformations.Trans.getTransValue("VarOnly")) ##  if we got to this point, they went straight to a variable.
        for parm in current_method.parameters:
            if rtnValue == parm: ## if the return value is a parameter, then it is a Transformation 11 assign.
                self.addToTransformationList(Transformations.Trans.getTransValue("AS"))

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

    def removeComments(self, gitFileHandle):
        line = gitFileHandle.getCurrentLine()
        foundQuotedComment = True
        while foundQuotedComment:
            action = line[0]       # either blank space, + or -
            noPlus = self.stripGitActionAndSpaces(line)
            endCommentFound = False
            if noPlus.startswith("'''") or noPlus.startswith("\"\"\""):
                foundQuotedComment = True
                if len(noPlus) > 3 and noPlus.endswith("'''") or noPlus.endswith("\"\"\""):   #one-line comment
                    line = gitFileHandle.readNextLine()
                    if line == False:
                        line = ' '
                        foundQuotedComment = False
                    else:
                        endCommentFound = True
                while not endCommentFound:
                    line = gitFileHandle.readNextLine()
                    if line == False:
                        line = ' '
                        break
                    noPlus = self.stripGitActionAndSpaces(line)
                    if (line[0] == action) and (line[0] != " "):
                        if noPlus.startswith("'''") or noPlus.startswith("\"\"\"") or noPlus.endswith("'''") or noPlus.endswith("\"\"\""):
                            line = gitFileHandle.readNextLine()
                            if line == False:
                                line = ' '
                                foundQuotedComment = False
                            else:
                                endCommentFound = True
                    else:
                        endCommentFound = True
            else:
                foundQuotedComment = False
        if re.search(r"\#", line):
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
        whileTrans = Transformations.Trans.getTransValue("WhileNoIf")
        for dLine in currentMethod.deletedLines:
            if dLine.deletedIf:
                if whileCondition == dLine.deletedIfContents:
                    return Transformations.Trans.getTransValue("I2W")
                else:
                    whileTrans = Transformations.Trans.getTransValue("WhileNoIf")
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
                self.addToTransformationList(Transformations.Trans.getTransValue("C2V"))
                return Transformations.Trans.getTransValue("I2W")
        return Transformations.Trans.getTransValue("WhileNoIf")


    def samePythonFile(self, line):
        " Are we still in the same python file changes or is this a new python file? "
        if line == False:              ## EOF
            line = ''
            return False
        if Commit.Commit.foundNewCommit(line) == True:
            return False
        evalLine = line.rstrip()
        if (evalLine.startswith("diff")):
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

    def isProdOrTest(self, pathName, fileName):
        pathNameLower = pathName.lower()
        fileNameLower = fileName.lower()
        prod = False
        if (pathNameLower.startswith('prod') or pathNameLower.startswith('softwareprocess') or
            pathNameLower.startswith('rcube')):
            if not (re.search("test",fileNameLower)):
                prod = True
        return prod

    def isProdFile(self):
        return self.prodFile

    def getFileType(self):
        if self.prodFile:
            return "Prod"
        else:
            return "Test"

    def getFileName(self):
        return self.fileName

    def setCommitDetails(self, my_commit_details):
        self.commitDetails.append(my_commit_details)

    def setMethodName(self, method_name):
        my_method = Method.Method(method_name, [])
        self.methods.append(my_method)

    def getCommitDetails(self):
        return self.commitDetails

    def numberOfTransformationsInPyFile(self):
        nbr_trans = 0
        for i in self.transformations:
            if i >= 0:
                nbr_trans += 1
        return nbr_trans

    def number_of_anti_transformations_in_pyfile(self):
        nbr_anti_trans = 0
        for i in self.transformations:
            if i < 0:
                nbr_anti_trans += 1
        return nbr_anti_trans

    def addToTransformationList(self, new_trans):
        self.transformations.append(new_trans)

    def get_transformations(self):
        return self.transformations

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

