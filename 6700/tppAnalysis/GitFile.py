import TATestCase
            if not (self.isCurrentAssignment()):                                    # advances to next line to check the commit date
                
                if self.currAssignment <= len(myAssignmentDict):
                    self.currAssignmentDate = myAssignmentDict[self.currAssignment]     # last date for the first assignment
            self.commitType = self.getCommitType()                      # advances to next line to get commit type
            self.myAssignment.addCommitToAssignment(self.analyzeCommit(self.commitType))
    
        addedLinesInFile = 0
        deletedLinesInFile = 0
            if len(noLeadingSpaces) > 0:                         ## no need to go through all of this for a blank line
                if (lineWithNoComments[0] == '-' and lineWithNoComments[1] != '-' and currentMethod.isATATestCase() == False):
                if lineWithNoComments[0] == '+' and lineWithNoComments[1] != '+' and currentMethod.isATATestCase() == False:
            addedLinesInFile = addedLinesInFile + method.getAddedLines()
            deletedLinesInFile = deletedLinesInFile + method.getDeletedLines()
            #if method.getAddedLines() == 0 and method.getDeletedLines() == 0:
            #        methodArray.remove(method)      # empty method
        return addedLinesInFile, deletedLinesInFile, methodArray
            if method.methodName in TATestCase.TATestCase.TATestCaseDict:       ## if they added one of the TA test cases, the number of lines in the test case will be removed from the number of test case lines that they wrote
                method.updateTATestLines(TATestCase.TATestCase.TATestCaseDict[method.methodName])
                method.setIsTATestCase(True)
                    if not (re.search(r"\bmetadata\b",evalLine)):
                        return True