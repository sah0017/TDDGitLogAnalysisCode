originalAssignmentName = "CA01"
        
        self.myAssignmentNameDict = Assignment.Assignment.get_assignment_name_dict()
        self.keyIndexList = self.myAssignmentNameDict.keys()
        self.keyIndexList.sort()

        __fileName = fileName
        self.gitFile = codecs.open(__fileName)
        print __fileName
        __currAssignmentName = "CA01"     # last date for the first assignment
        __myAssignment = Assignment.Assignment(__currAssignmentName)
        
        __commits = 0
            __assignmentName = self.findCurrentAssignment()                                    # advances to next line to check the commit date
            if __currAssignmentName != __assignmentName:    
                __currAssignmentName = __assignmentName
                self.myAssignmentsList.append(__myAssignment)
                __commits = 0
                __myAssignment = Assignment.Assignment(__currAssignmentName)
            __commitType = self.getCommitType()                      # advances to next line to get commit type
            __commits = __commits + 1
            __myAssignment.addCommitToAssignment(self.analyzeCommit(__currAssignmentName,__commitType, __commits))
        self.myAssignmentsList.append(__myAssignment)                # save last Assignment in the file to Assignments List
    def analyzeCommit(self, assignmentName, commitType, commitNbr):
        self.myNewCommit = Commit.Commit(commitNbr)
                addedLines, deletedLines, TATestLines, prodFile, notSBFile = self.analyzePyFile(path,fileName,assignmentName, commitNbr)
                        self.myNewCommit.set_added_tatest_loc(TATestLines)

        self.myNewCommit.add_number_of_transformations(len(self.myTransformations))
    def analyzePyFile(self, path, fileName, assignmentName, commitNbr):
        fileIndex = self.findExistingFileToAddCommitDetails(fileName) 
        if (fileIndex == -1):
            fileIndex = self.addNewFile(fileName, prodFile, commitNbr)
        fileAddedLines, fileDeletedLines, fileTATestLines, methods = self.evaluateTransformationsInAFile(prodFile)
        self.myFiles[fileIndex].setCommitDetails(assignmentName, commitNbr, fileAddedLines, fileDeletedLines, fileTATestLines, methods)
        return fileAddedLines, fileDeletedLines, fileTATestLines, prodFile, True
        taTestLinesInFile = 0
            taTestLinesInFile = taTestLinesInFile + method.getTATestLines()
        return addedLinesInFile, deletedLinesInFile, taTestLinesInFile, methodArray
    def findCurrentAssignment(self):
        currAssignmentName = None
        if commitDate <= self.keyIndexList[0]:
            currAssignmentName = originalAssignmentName
            for k in range(0, len(self.keyIndexList)-1):
                if (self.keyIndexList[k] <= commitDate <= self.keyIndexList[k+1]):
                    currAssignmentName = self.myAssignmentNameDict.get(self.keyIndexList[k+1])
        return currAssignmentName
    def addNewFile(self, fileName, prodFile, commitNbr):
        self.newFile = PyFile.PyFile(fileName, prodFile, commitNbr)