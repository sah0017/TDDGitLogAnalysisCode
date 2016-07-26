'''
Created on Jul 15, 2016

@author: susanha
'''

import re, os, ConfigParser 

if __name__ == '__main__':
    myConfig = ConfigParser.ConfigParser() 
    myConfig.read("TDDanalysis.cfg")
    myDrive = myConfig.get("Location","Root")
    myHome = myConfig.get("Location","Home")
    mySemester = myConfig.get("Location","Semester")
    myAssignment = myConfig.get("Location","Assignment")

    dirList = open(myAssignment+".dirList","w")
    includePath=""
    for root, myDir, files in os.walk(myDrive+os.sep+myHome+os.sep+mySemester+os.sep+myAssignment+os.sep+"submissions"):
        if re.search("test", root):
            if not re.search("__MACOSX",root):
                nameSplit = root.split(os.sep)
                if nameSplit[len(nameSplit)-1] == "__pycache__":
                    nameSplit = nameSplit[:len(nameSplit)-1]
                for i in range(0,len(nameSplit)-1):
                    includePath = includePath + nameSplit[i] + os.sep
                print includePath
                dirList.write(includePath+"\n")
        includePath = ""
    dirList.close()