'''
Created on Jun 24, 2014

@author: susanha
'''
import os
import glob
import Factor
import radon
from radon.complexity import *


class AnalyzedFiles():
    
    def init(self):
        pass
        
 
        
class AnalyzeFiles(object):
    
    
    def complexityAssessment(self):
        visitedFiles = []
        fileName = ""
        for path, dirs, files in os.walk("C:\\6700"):
        #for pyFile in glob.glob("*.py"):
            #with open(files) as fp:
        
            #   
            for f in files:
                if f.endswith(".py"):
                    fileName = path + "\\" + f
                    fp = open(fileName)
                    self.code = fp.read()
                    try:
                        visitor = ComplexityVisitor.from_code(self.code)
                        visitedFiles.append(visitor)
                        print radon.complexity.sorted_results(radon.complexity.cc_visit(self.code))
                    except:
                        print "Exception:  " + fileName
            
        for visitor in visitedFiles:
            print visitor.classname, radon.complexity.cc_rank(visitor.total_complexity)
        '''
            print visitor.functions
            print visitor.complexity
            print visitor.functions_complexity
            print visitor.total_complexity
        '''
        '''thisComplexity = visitor.complexity.cc_visit()
        print thisComplexity  '''

if __name__ == '__main__':
    AnalyzeFiles().complexityAssessment()