'''
Created on Jul 15, 2016

@author: susanha

This file creates a directory list of the submissions.  The list is used by the CodeCoverage shell/batch
script to loop through the directories and assess their Code Coverage by calling CodeCoverage.py.
'''

import re, os, ConfigParser 

if __name__ == '__main__':
    myConfig = ConfigParser.ConfigParser() 
    myConfig.read("TDDanalysis.cfg")
    myDrive = myConfig.get("Location","Root")
    myHome = myConfig.get("Location","Home")
    mySemester = myConfig.get("Location","Semester")
    myAssignment = myConfig.get("Location","Assignment")
    root = os.path.join(myDrive, myHome, mySemester, myAssignment, "submissions")

    dirList = open(myAssignment+".dirList","w")
    includePath=""
    myDir = os.listdir(root)

    for name in myDir:
        includePath = os.path.join(root,name)
        print includePath
        dirList.write(includePath+"\n")
        includePath = ""
    dirList.close()
