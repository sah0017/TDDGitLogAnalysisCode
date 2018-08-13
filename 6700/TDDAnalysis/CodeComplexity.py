"""
Created on Jul 7, 2015

@author: susan hammond
"""

from radon.complexity import cc_rank, cc_visit, SCORE
from radon.cli import Config
from radon.cli.harvest import CCHarvester
from radon.cli.harvest import MIHarvester
from sys import exc_info


class CodeComplexity(object):
    """
    class docs
    """

    def __init__(self, my_drive, my_semester):
        """
        Constructor
        """
        self.my_drive = my_drive
        self.my_semester = my_semester

    def analyze_complexity(self, args):
        
        def av(mod_cc, len):
            return mod_cc / len if len != 0 else 0
        
        config = Config(
            exclude=args.exclude,
            ignore=args.ignore,
            order=SCORE,
            no_assert=args.no_assert,
            multi=args.multi,
            show_closures=False,
            min='A',
            max='F')
        total_cc = 0.
        total_blocks = 0
        module_averages = []
        
        try:
            h = CCHarvester([args.path], config)
            m = MIHarvester([args.path], config)
            cc_results = h._to_dicts()
            mi_results = []
            for filename, mi_data in m.results:
                if mi_data:
                    # continue
                    mi_results.append((mi_data['mi'], mi_data['rank']))
            for module, blocks in cc_results.items():
                module_cc = 0.
                if len(blocks) != 0:
                    for block in blocks:
                        if block != "error":
                            module_cc += block['complexity']
                            r = cc_rank(block['complexity'])
                module_averages.append((module, av(module_cc, len(blocks))))
                total_cc += module_cc
                total_blocks += len(blocks)
            return module_averages, mi_results
        except Exception as e:
            print (exc_info()[0], e)
            return None, None
