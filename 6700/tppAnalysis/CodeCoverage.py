'''
Created on Jun 23, 2016

@author: susanha
'''

import coverage

class CodeCoverage(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    def analyzeCodeCoverage(self,dataFile, fileSource, include):
        cov = coverage.Coverage(data_file=dataFile, source=fileSource, include="*.py", branch=True )
        '''
        cov.load()
        cov.start()
        cov.analysis2(fileSource)
        cov.stop()
        cov.save()
        cov.report(morfs, show_missing, ignore_errors, file, omit, include, skip_covered)
        '''
    