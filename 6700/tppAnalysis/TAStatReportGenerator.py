'''
Created on Jul 1, 2016

@author: susanha

This program is called from the AutoGrader batch (for Windows) or shell script (for Mac).  AutoGrader
loops through the list of submissions (created by GetDirectoryList) and passes in the student path and
correct assignment to analyze.
The runTaTests method loads the TA test files and runs the student's tests against the
TA Test code.
'''
import sys, os, re, unittest, coverage
import ConfigParser
import TAAutoGrader

class TAStatReportGenerator(object):
    myConfig = ConfigParser.ConfigParser()
    myConfig.read("TDDanalysis.cfg")
    myDrive = myConfig.get("Location","Root")
    myHome = myConfig.get("Location","Home")
    mySemester = myConfig.get("Location","Semester")
    myAssignment = myConfig.get("Location","Assignment")
    TATestLocation = myConfig.get("TA Test Case Location", "Test Directory")

    myAutoGrader = TAAutoGrader.TAAutoGrader()
    failStats = myAutoGrader.retrieveTAReportObject(TAAutoGrader.TAAutoGrader.FAIL)
    errorStats = myAutoGrader.retrieveTAReportObject(TAAutoGrader.TAAutoGrader.ERROR)

    with open(os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + TATestLocation +
                                 os.sep + myAutoGrader.ERROR + ".TAreport"), "w") as TAreportoutFile:

        TAreportoutFile.write("\n\rTest Case Name \t Number of Errors " + "\n\r")
        if errorStats != None:
            for key, val in errorStats:
                TAreportoutFile.write(str(key) + "\t" + str(val) + "\n\r")
        else:
            TAreportoutFile.write("No errors to report\n\r")


    with open(os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + TATestLocation +
                                 os.sep + myAutoGrader.FAIL + ".TAreport"), "w") as TAreportoutFile:

        TAreportoutFile.write("\n\rTest Case Name \t Number of Failures " + "\n\r")
        if failStats != None:
            for key, val in failStats:
                TAreportoutFile.write(str(key) + "\t" + str(val) + "\n\r")
        else:
            TAreportoutFile.write("No failures to report\n\r")

if __name__ == '__main__':
    myRpt = TAStatReportGenerator()
