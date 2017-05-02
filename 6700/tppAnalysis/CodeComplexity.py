'''
Created on Jul 7, 2015

@author: susanha
'''

from radon.complexity import cc_rank, cc_visit, SCORE
from radon.cli import Config
from radon.cli.harvest import CCHarvester
from radon.cli.harvest import MIHarvester
import os
import json

class CodeComplexity(object):
    '''
    classdocs
    '''


    def __init__(self, myDrive, mySemester):
        '''
        Constructor
        '''
        self.myDrive = myDrive
        self.mySemester = mySemester

     
    def analyzeComplexity(self, args):
        
        def av(n,m): 
            return n/m if m !=0 else 0
        
        config = Config(
            exclude = args.exclude,
            ignore = args.ignore,
            order=SCORE,
            no_assert = args.no_assert,
            multi = args.multi,
            show_closures = False,
            min='A',
            max='F')
        total_cc = 0.
        total_blocks = 0
        module_averages = []
        
        try:
            h = CCHarvester([args.path],config)
            m = MIHarvester([args.path],config)
            cc_results = h._to_dicts()
            mi_results = []
            for filename, mi_data in m.results:
                if not mi_data:
                    continue
                mi_results.append((mi_data['mi'], mi_data['rank']))
            for module, blocks in cc_results.items():
                module_cc = 0.
                if len(blocks) != 0:
                    for block in blocks:
                        module_cc += block['complexity']
                        r = cc_rank(block['complexity'])
                module_averages.append((module, av(module_cc, len(blocks))))
                total_cc += module_cc
                total_blocks += len(blocks)
            return module_averages, mi_results
        except Exception as e:
            print e   