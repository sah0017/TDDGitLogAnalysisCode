"""
Created on Jul 15, 2016

@author: susanha

This file creates a directory list of the submissions.  The list is used by the CodeCoverage shell/batch
script to loop through the directories and assess their Code Coverage by calling CodeCoverage.py.
"""

import os
import ConfigParser

if __name__ == '__main__':
    myConfig = ConfigParser.ConfigParser() 
    myConfig.read("TDDanalysis.cfg")
    myDrive = myConfig.get("Location", "Root")
    myHome = myConfig.get("Location", "Home")
    mySemester = myConfig.get("Location", "Semester")
    myAssignment = myConfig.get("Location", "Assignment")
    root = os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep +  myAssignment + os.sep + "submissions")

    dirList = open(myAssignment+".dirList", "w")
    myDir = os.listdir(root)

    for name in myDir:
        include_path = os.path.join(root + os.sep + name)
        print include_path
        dirList.write(include_path + "\n")
        include_path = ""
    dirList.close()
