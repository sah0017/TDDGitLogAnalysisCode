'''
Created on Apr 25, 2016

@author: susanha
'''

import CreateAnalysisReport



if __name__ == '__main__':
    
    myDrive = "g:\\"
    printToFile = raw_input("Print output to file?  ")
    mySemester = "6700Spring16"
    myDirectory = "CA02"
    CreateAnalysisReport.createAnalysisReport(myDrive, printToFile,mySemester,myDirectory)