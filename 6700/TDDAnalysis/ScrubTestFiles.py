"""
Created on Jul 6, 2016

@author: susan hammond
"""

import os
import re
import ConfigParser


def scrub_single_test_file(path, file_name):
    with open(os.path.join(path + os.sep + file_name, "rb+")) as testFile:
        lines_in_file = testFile.readlines()
    for line in range(len(lines_in_file)):
        if re.search("import", lines_in_file[line]) and not lines_in_file[line].lstrip().startswith("#"):
            if re.search(r"\btest\b|\bprod\b", lines_in_file[line]):
                line_parts = lines_in_file[line].split(".")

                if lines_in_file[line].startswith("import"):
                    module_with_no_trailing_characters = line_parts[len(line_parts)-1].rstrip()
                    lines_in_file[line] = "import " + module_with_no_trailing_characters + '\r'
                else:
                    module_with_no_trailing_characters = line_parts[len(line_parts)-1].split(" ")
                    lines_in_file[line] = "from " + module_with_no_trailing_characters[0] + " import " + module_with_no_trailing_characters[2] + '\r'
    with open(path + "\\" + file_name, "w") as testFile:
        testFile.writelines(lines_in_file)
        

def scrub_test_files(path):
    for root, myDir, files in os.walk(path):
        if re.search(r"\btest\b|\bprod\b", root):
            for f in files:
                name_split = f.split(".")
                if name_split[len(name_split)-1] == "py" and f != "__init__.py":
                    print root, f
                    scrub_single_test_file(root, f)
            

if __name__ == '__main__':
    myConfig = ConfigParser.ConfigParser() 
    myConfig.read("TDDanalysis.cfg")
    myDrive = myConfig.get("Location", "Root")
    myHome = myConfig.get("Location", "Home")
    mySemester = myConfig.get("Location", "Semester")
    myAssignment = myConfig.get("Location", "Assignment")
    scrub_test_files(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + myAssignment + os.sep + "submissions")
    # scrub_single_test_file("g:\\git\\6700Spring16\\CA03\\submissions\\hallmichael_late_2242176_73398598_CA03_Mlh0045\\SoftwareProcess\\CA03\\test", "LatitudeTest.py")
