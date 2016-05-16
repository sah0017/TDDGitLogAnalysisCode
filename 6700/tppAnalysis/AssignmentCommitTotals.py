'''
Created on Apr 12, 2016

@author: susanha
'''


class AssignmentCommitTotals(object):
    '''
    These are overall totals for all the Assignments.
    '''
    __totalSubmissions = 0
    __totalCommits = 0
    __totalRLCommits =0 
    __totalGLCommits = 0
    __totalRefCommits = 0
    __totalOtherCommits = 0
    __AvgLinesPerCommit = 0.0
    __AvgTransPerCommit = 0.0
    __RatioTestToProd = 0.0
    __totalDeletedLines = 0
    __totalNbrTransformations = 0
    __totalProdFiles = 0
    __totalTestFiles = 0
    __totalProdLOC = 0
    __totalTestLOC = 0
    __totalLinesOfCodeAdded = 0
    __totalTransByType = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    __totalAntiTransByType = [0,0,0,0,0,0,0,0,0]


    def __init__(self):
        '''
        These are overall totals for an individual Assignment
        
        '''
        
        #self.assignment = assignment
        self.__nbrCommits = 0
        self.__RLCommit = 0
        self.__GLCommit = 0
        self.__refCommit = 0
        self.__otherCommit = 0
        self.__addedLinesInAssignment = 0
        self.__deletedLinesInAssignment = 0
        self.__addedTestLOCInAssignment = 0
        self.__deletedTestLOCInAssignment = 0
        self.__nbrTestFilesInAssignment = 0
        self.__nbrProdFilesInAssignment = 0
        self.__avgLinesPerCommit = 0
        self.__avgTransPerCommit = 0
        self.__ratioTestToProd = 0
        self.__totalDelLines = 0
        self.__totalTransByTypeInAssignment = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.__totalAntiTransByTypeInAssignment = [0,0,0,0,0,0,0,0,0]
        
    @classmethod
    def set_total_submissions(cls, value):
        cls.__totalSubmissions = cls.__totalSubmissions + value
      
    @classmethod
    def set_total_deleted_lines(cls, value):
        cls.__totalDeletedLines = cls.__totalDeletedLines + value
        
    @classmethod
    def set_total_prod_LOC(cls, value):
        cls.__totalProdLOC = cls.__totalProdLOC + value
        
    @classmethod
    def set_total_test_LOC(cls, value):
        cls.__totalTestLOC = cls.__totalTestLOC + value
                
    @classmethod
    def set_total_nbr_transformations(cls, value):
        cls.__totalNbrTransformations = cls.__totalNbrTransformations + value
    
    @classmethod
    def set_total_prod_files(cls, value):
        cls.__totalProdFiles = cls.__totalProdFiles + value
    
    @classmethod
    def set_total_test_files(cls, value):
        cls.__totalTestFiles = cls.__totalTestFiles + value
    
    @classmethod
    def set_total_LOC(cls, value):
        cls.__totalLinesOfCodeAdded = cls.__totalLinesOfCodeAdded + value
    
    
                
    @classmethod
    def set_total_commits(cls, value):
        cls.__totalCommits = cls.__totalCommits + value
    
    @classmethod
    def set_total_RL_commits(cls, value):
        cls.__totalRLCommits = cls.__totalRLCommits + value
    
    @classmethod
    def set_total_GL_commits(cls, value):
        cls.__totalGLCommits = cls.__totalGLCommits + value
    
    @classmethod
    def set_total_ref_commits(cls, value):
        cls.__totalRefCommits = cls.__totalRefCommits + value
        
    @classmethod
    def set_total_other_commits(cls, value):
        cls.__totalOtherCommits = cls.__totalOtherCommits + value
        
    @classmethod
    def set_total_trans_by_type(cls, value, tranType):
        cls.__totalTransByType[tranType] = cls.__totalTransByType[tranType] + value   
    
    @classmethod
    def set_total_antitrans_by_type(cls, value, tranType):
        cls.__totalAntiTransByType[tranType] = cls.__totalAntiTransByType[tranType] + value
        
    @classmethod
    def get_total_submissions(cls):
        return cls.__totalSubmissions 
        
    @classmethod
    def get_total_prod_LOC(cls):
        return cls.__totalProdLOC 
        
    @classmethod
    def get_total_test_LOC(cls):
        return cls.__totalTestLOC 
                
    @classmethod
    def get_total_nbr_transformations(cls):
        return cls.__totalNbrTransformations 
    
    @classmethod
    def get_total_prod_files(cls):
        return cls.__totalProdFiles 
    
    @classmethod
    def get_total_test_files(cls):
        return cls.__totalTestFiles 
    
    @classmethod
    def get_total_LOC(cls):
        return cls.__totalLinesOfCodeAdded 
    
    
                
    @classmethod
    def get_total_commits(cls):
        return cls.__totalCommits 
    
    @classmethod
    def get_total_RL_commits(cls):
        return cls.__totalRLCommits
    
    @classmethod
    def get_total_GL_commits(cls):
        return cls.__totalGLCommits 
    
    @classmethod
    def get_total_ref_commits(cls):
        return cls.__totalRefCommits 
        
    @classmethod
    def get_total_other_commits(cls):
        return cls.__totalOtherCommits 
        
    @classmethod
    def get_total_avg_lines_per_commit(cls):
        cls.__totalAvgLinesPerCommit = cls.__totalLinesOfCodeAdded / cls.__totalCommits
        return cls.__totalAvgLinesPerCommit
        
    @classmethod
    def get_total_avg_trans_per_commit(cls):
        cls.__totalAvgTransPerCommit = cls.__totalNbrTransformations / cls.__totalCommits
        return cls.__totalAvgTransPerCommit
    
    @classmethod
    def get_total_ratio_test_to_prod(cls):
        cls.__ratioTestToProd = cls.__totalTestLOC / cls.__totalProdLOC        
        return cls.__ratioTestToProd
    
    @classmethod
    def get_total_trans_by_type(cls):
        return cls.__totalTransByType

    @classmethod
    def get_total_antitrans_by_type(cls):
        return cls.__totalAntiTransByType
    
    def get_assignment(self):
        return self.__assignment


    def get_nbr_commits(self):
        return self.__nbrCommits


    def get_rlcommit(self):
        return self.__RLCommit


    def get_glcommit(self):
        return self.__GLCommit


    def get_ref_commit(self):
        return self.__refCommit


    def get_other_commit(self):
        return self.__otherCommit


    def get_avg_lines_per_commit(self):
        return self.__avgLinesPerCommit


    def get_avg_trans_per_commit(self):
        return self.__avgTransPerCommit


    def get_ratio_test_to_prod(self):
        return self.__ratioTestToProd


    def get_total_del_lines(self):
        return self.__totalDelLines
    
    def get_total_nbr_transformations_in_assignment(self):
        __nbrTrans = 0
        for trans in self.__totalTransByTypeInAssignment:
            __nbrTrans = __nbrTrans + self.__totalTransByTypeInAssignment[trans]
        return __nbrTrans

    def get_added_lines_in_assignment(self):
        return self.__addedLinesInAssignment


    def get_deleted_lines_in_assignment(self):
        return self.__deletedLinesInAssignment


    def get_added_test_locin_assignment(self):
        return self.__addedTestLOCInAssignment


    def get_deleted_test_locin_assignment(self):
        return self.__deletedTestLOCInAssignment


    def get_nbr_test_files_in_assignment(self):
        return self.__nbrTestFilesInAssignment


    def get_nbr_prod_files_in_assignment(self):
        return self.__nbrProdFilesInAssignment
    
    def get_total_trans_by_type_in_assignment(self):
        return self.__totalTransByTypeInAssignment


    def get_total_anti_trans_by_type_in_assignment(self):
        return self.__totalAntiTransByTypeInAssignment




    def set_assignment(self, value):
        self.__assignment = value


    def set_nbr_commits(self, value):
        self.__nbrCommits = value
        AssignmentCommitTotals.set_total_commits(value)
        


    def set_rlcommit(self, value):
        self.__RLCommit = value
        AssignmentCommitTotals.set_total_RL_commits(value)


    def set_glcommit(self, value):
        self.__GLCommit = value
        AssignmentCommitTotals.set_total_GL_commits(value)


    def set_ref_commit(self, value):
        self.__refCommit = value
        AssignmentCommitTotals.set_total_ref_commits(value)


    def set_other_commit(self, value):
        self.__otherCommit = value
        AssignmentCommitTotals.set_total_other_commits(value)


    def set_avg_lines_per_commit(self, value):
        self.__avgLinesPerCommit = value


    def set_avg_trans_per_commit(self, value):
        self.__avgTransPerCommit = value


    def set_ratio_test_to_prod(self, value):
        self.__ratioTestToProd = value


    def set_total_del_lines(self, value):
        self.__totalDelLines = value
        AssignmentCommitTotals.set_total_deleted_lines(value)
        
    def set_added_lines_in_assignment(self, value):
        self.__addedLinesInAssignment = self.__addedLinesInAssignment + value


    def set_deleted_lines_in_assignment(self, value):
        self.__deletedLinesInAssignment = self.__deletedLinesInAssignment + value


    def set_added_test_locin_assignment(self, value):
        self.__addedTestLOCInAssignment = self.__addedTestLOCInAssignment + value


    def set_deleted_test_locin_assignment(self, value):
        self.__deletedTestLOCInAssignment = self.__deletedTestLOCInAssignment + value


    def set_nbr_test_files_in_assignment(self, value):
        self.__nbrTestFilesInAssignment = self.__nbrTestFilesInAssignment + value


    def set_nbr_prod_files_in_assignment(self, value):
        self.__nbrProdFilesInAssignment = self.__nbrProdFilesInAssignment + value


    def set_total_trans_by_type_in_assignment(self, value):
        self.__totalTransByTypeInAssignment = value


    def set_total_anti_trans_by_type_in_assignment(self, value):
        self.__totalAntiTransByTypeInAssignment = value

        


    def del_assignment(self):
        del self.__assignment


    def del_nbr_commits(self):
        del self.__nbrCommits


    def del_rlcommit(self):
        del self.__RLCommit


    def del_glcommit(self):
        del self.__GLCommit


    def del_ref_commit(self):
        del self.__refCommit


    def del_other_commit(self):
        del self.__otherCommit


    def del_avg_lines_per_commit(self):
        del self.__avgLinesPerCommit


    def del_avg_trans_per_commit(self):
        del self.__avgTransPerCommit


    def del_ratio_test_to_prod(self):
        del self.__ratioTestToProd


    def del_total_del_lines(self):
        del self.__totalDelLines
        
    def del_added_lines_in_assignment(self):
        del self.__addedLinesInAssignment


    def del_deleted_lines_in_assignment(self):
        del self.__deletedLinesInAssignment


    def del_added_test_locin_assignment(self):
        del self.__addedTestLOCInAssignment


    def del_deleted_test_locin_assignment(self):
        del self.__deletedTestLOCInAssignment


    def del_nbr_test_files_in_assignment(self):
        del self.__nbrTestFilesInAssignment


    def del_nbr_prod_files_in_assignment(self):
        del self.__nbrProdFilesInAssignment

        
        

    def del_total_trans_by_type_in_assignment(self):
        del self.__totalTransByTypeInAssignment


    def del_total_anti_trans_by_type_in_assignment(self):
        del self.__totalAntiTransByTypeInAssignment

    


    assignment = property(get_assignment, set_assignment, del_assignment, "assignment's docstring")
    nbrCommits = property(get_nbr_commits, set_nbr_commits, del_nbr_commits, "nbrCommits's docstring")
    RLCommit = property(get_rlcommit, set_rlcommit, del_rlcommit, "RLCommit's docstring")
    GLCommit = property(get_glcommit, set_glcommit, del_glcommit, "GLCommit's docstring")
    refCommit = property(get_ref_commit, set_ref_commit, del_ref_commit, "refCommit's docstring")
    otherCommit = property(get_other_commit, set_other_commit, del_other_commit, "otherCommit's docstring")
    avgLinesPerCommit = property(get_avg_lines_per_commit, set_avg_lines_per_commit, del_avg_lines_per_commit, "avgLinesPerCommit's docstring")
    avgTransPerCommit = property(get_avg_trans_per_commit, set_avg_trans_per_commit, del_avg_trans_per_commit, "avgTransPerCommit's docstring")
    ratioTestToProd = property(get_ratio_test_to_prod, set_ratio_test_to_prod, del_ratio_test_to_prod, "ratioTestToProd's docstring")
    totalDelLines = property(get_total_del_lines, set_total_del_lines, del_total_del_lines, "totalDelLines's docstring")
    totalTransByTypeInAssignment = property(get_total_trans_by_type_in_assignment, set_total_trans_by_type_in_assignment, del_total_trans_by_type_in_assignment, "totalTransByTypeInAssignment's docstring")
    totalAntiTransByTypeInAssignment = property(get_total_anti_trans_by_type_in_assignment, set_total_anti_trans_by_type_in_assignment, del_total_anti_trans_by_type_in_assignment, "totalAntiTransByTypeInAssignment's docstring")
    addedLinesInAssignment = property(get_added_lines_in_assignment, set_added_lines_in_assignment, del_added_lines_in_assignment, "addedLinesInAssignment's docstring")
    deletedLinesInAssignment = property(get_deleted_lines_in_assignment, set_deleted_lines_in_assignment, del_deleted_lines_in_assignment, "deletedLinesInAssignment's docstring")
    addedTestLOCInAssignment = property(get_added_test_locin_assignment, set_added_test_locin_assignment, del_added_test_locin_assignment, "addedTestLOCInAssignment's docstring")
    deletedTestLOCInAssignment = property(get_deleted_test_locin_assignment, set_deleted_test_locin_assignment, del_deleted_test_locin_assignment, "deletedTestLOCInAssignment's docstring")
    nbrTestFilesInAssignment = property(get_nbr_test_files_in_assignment, set_nbr_test_files_in_assignment, del_nbr_test_files_in_assignment, "nbrTestFilesInAssignment's docstring")
    nbrProdFilesInAssignment = property(get_nbr_prod_files_in_assignment, set_nbr_prod_files_in_assignment, del_nbr_prod_files_in_assignment, "nbrProdFilesInAssignment's docstring")
    
    
    