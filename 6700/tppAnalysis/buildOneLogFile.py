'''
Created on Jan 8, 2015

@author: Susan
'''

import os
import subprocess


if __name__ == '__main__':
    myDirectory = "CA03"
    myAssignment = "CA03"
    os.chdir("G:\\git\\6700Fall15\\CA03\\submissions\\ahlawat--kushagar\\softwareProcess\\.git")
    p=subprocess.Popen(["git","log","-p","-m","--reverse","--pretty=format:\"%s\""],stdout=subprocess.PIPE)
    outFile = open("g:\\git\\6700Fall15\\"+myDirectory+"\\kza0026Log", "w")
    for line in p.stdout.readlines():
        outFile.write(line)
    outFile.close()