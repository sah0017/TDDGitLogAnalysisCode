import Method
        methodNames = []
            self.fileIndex = self.addNewFile(fileName, testFile)
            self.fileIndex = self.findExistingFileToAddCommitDetails(fileName) 
        fileAddedLines, fileDeletedLines, methodNames = self.evaluateTransformations()
        self.myFiles[self.fileIndex].setCommitDetails(self.commits, fileAddedLines, fileDeletedLines, methodNames)
        methodNames = []
        params = []
            commentSplit = self.line.split("##")
            lineWithNoComments = commentSplit[0]
            noLeadingPlus = lineWithNoComments[1:]
            if re.search(r"\bdef\b", lineWithNoComments):
                noLeadingSpaces = noLeadingPlus.strip()
                methodName = noLeadingSpaces.split(" ")
                methodName = methodName[1].split("(")
                methodNames.append(methodName[0])
                methodName[len(methodName)-1] = methodName[len(methodName)-1]
                params = methodName[1].split(",")
                for x in params:
                    if re.search("self",x):
                        params.remove(x)
                if len(params) > 0:
                    lastParam = params[len(params)-1]
                    lastParam = lastParam[0:len(lastParam)-2]     ## removes ): from last parameter
                    params[len(params)-1] = lastParam
                print params
                ##self.myFiles[self.fileIndex].setMethodName(methodName[0])
                ##print methodName[0]
            if lineWithNoComments[0] == '-':
                if re.search("return", lineWithNoComments):
                    deletedLiteral = self.checkForConstantOnReturn(lineWithNoComments)
                if re.search(r"\bif .", lineWithNoComments):
                    ifConditionalParts = lineWithNoComments.split("if")
                if re.search(r"\bwhile .", lineWithNoComments):
                    whileConditionalParts = lineWithNoComments.split("while")
            if lineWithNoComments[0] == '+':
                if re.search(r"\bpass\b",lineWithNoComments):
                if re.search(r"\breturn\b", lineWithNoComments):
                elif (re.search(r"=",noLeadingPlus)):
                    if not (re.search(r"['\"]",noLeadingPlus)):       ## Not Add Computation if the character is inside a quoted string
                        if not (re.search(r"==",noLeadingPlus)):      ## evaluation, not assignment
                            self.myTransformations.append(myTrans.AComp)
                            assignmentVars = noLeadingPlus.split("=")
                            assignmentVar = assignmentVars[0].strip()
                            for x in params:
                                if x == assignmentVar:
                                    self.myTransformations.append(myTrans.AS)
                elif (re.search(r"\belif\b",noLeadingPlus)):
                    self.myTransformations.append(myTrans.ACase)
        return addedLines, deletedLines, methodNames