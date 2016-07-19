'''
Created on Jul 15, 2016

@author: susanha
'''

import re, os 

if __name__ == '__main__':
    assignment = "CA05"
    dirList = open("g:\\git\\6700Spring16\\"+assignment+".dirList","w")
    includePath=""
    for root, myDir, files in os.walk("g:\\git\\6700Spring16\\"+assignment+"\\submissions"):
        if re.search("test", root):
            if not re.search("__MACOSX",root):
                nameSplit = root.split("\\")
                if nameSplit[len(nameSplit)-1] == "__pycache__":
                    nameSplit = nameSplit[:len(nameSplit)-1]
                for i in range(0,len(nameSplit)-1):
                    includePath = includePath + nameSplit[i] + "\\"
                print includePath
                dirList.write(includePath+"\n")
        includePath = ""
    dirList.close()