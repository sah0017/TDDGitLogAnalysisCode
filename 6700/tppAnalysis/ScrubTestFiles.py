'''
Created on Jul 6, 2016

@author: susanha
'''

import os, re, ConfigParser

def scrubSingleTestFile(path,fileName):
    with open(os.path.join(path+os.sep+fileName,"rb+")) as testFile:
        linesInFile = testFile.readlines()
    for line in range(len(linesInFile)):
        if re.search("import",linesInFile[line]) and not linesInFile[line].lstrip().startswith("#"):
            if re.search(r"\btest\b|\bprod\b",linesInFile[line]):
                lineParts = linesInFile[line].split(".")

                if linesInFile[line].startswith("import"):
                    moduleWithNoTrailingCharacters = lineParts[len(lineParts)-1].rstrip()
                    linesInFile[line] = "import " + moduleWithNoTrailingCharacters + '\r'
                else:
                    moduleWithNoTrailingCharacters = lineParts[len(lineParts)-1].split(" ")
                    linesInFile[line] = "from " + moduleWithNoTrailingCharacters[0] + " import " + moduleWithNoTrailingCharacters[2]+ '\r'
    with open(path+"\\"+fileName,"w") as testFile:
        testFile.writelines(linesInFile)
        

def scrubTestFiles(path):
    for root, myDir, files in os.walk(path):
        if re.search(r"\btest\b|\bprod\b", root):
            for f in files:
                namesplit = f.split(".")
                if namesplit[len(namesplit)-1] == "py" and f != "__init__.py":
                    print root,f
                    scrubSingleTestFile(root, f)
            


if __name__ == '__main__':
    myConfig = ConfigParser.ConfigParser() 
    myConfig.read("TDDanalysis.cfg")
    myDrive = myConfig.get("Location","Root")
    myHome = myConfig.get("Location","Home")
    mySemester = myConfig.get("Location","Semester")
    myAssignment = myConfig.get("Location","Assignment")
    scrubTestFiles(myDrive+os.sep+myHome+os.sep+mySemester+os.sep+myAssignment+os.sep+"submissions")
    #scrubSingleTestFile("g:\\git\\6700Spring16\\CA03\\submissions\\hallmichael_late_2242176_73398598_CA03_Mlh0045\\SoftwareProcess\\CA03\\test", "LatitudeTest.py")