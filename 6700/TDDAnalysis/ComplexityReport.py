"""
Created on Apr 25, 2016

@author: susan hammond

"""

import CodeComplexity
import os
import re
from radon.complexity import cc_rank
from statistics import median


class RadonAnalysis(object):
    
    def __init__(self):
        self.path = "/Users/shammond/GoogleDrive/6700Spring17"
        self.exclude = "*.pyc"
        self.ignore = ""
        self.no_assert = True
        self.multi = False


def create_complexity_analysis_report():
    config_args = RadonAnalysis()

    my_drive = "/Users/shammond/GoogleDrive"
    my_semester = "6700Spring17"
    my_assignment = "Assignment5"
    out_file = open(my_drive + os.sep + my_semester + os.sep + my_assignment + os.sep + "code_complexity.csv", "w+")
    out_file.write("Module Name, CC Rank, CC Index\n")
    for root, myDir, files in os.walk(my_drive + os.sep + my_semester + os.sep + my_assignment + os.sep + "submissions"):
        name_split = root.split(os.sep)
        my_complexity_analysis = CodeComplexity.CodeComplexity(my_drive, my_semester)
        if re.search("softwareprocess", root):
            cum_score = 0.
            nbr_prod_files = 0
            complexity_score_list = []
            for myFile in files:
                if myFile.endswith(".py") and (not myFile.startswith("._")) and (myFile != '__init__.py'):
                    # os.chdir(myDir)
                    print root + os.sep + myFile
                    config_args.path = os.path.join(root, myFile)
                    results, mi_results = my_complexity_analysis.analyze_complexity(config_args)
                    if results is not None and len(results) > 0:
                        for module, ma in results:
                            cum_score += ma
                            nbr_prod_files += 1
                            complexity_score_list.append(ma)
                            mar = cc_rank(ma)
                            out_file.write(module + "," + mar + "," + format(ma, ".2f") + "\n")
                    else:
                        out_file.write(name_split[7] + os.sep + myFile + ", Missing, " + "\n")
            if nbr_prod_files > 0:
                avg_score = cum_score / nbr_prod_files
                med_score = median(complexity_score_list)
                max_score = max(complexity_score_list)
                out_file.write(name_split[7] + ", Average:  ," + format(avg_score, ".2f") + ", Median:  ,"
                           + format(med_score, ".2f") + ", Max:  ," + format(max_score, ".2f") + "\n")
    out_file.close()


if __name__ == '__main__':
    
    create_complexity_analysis_report()
