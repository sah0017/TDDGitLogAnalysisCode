'''
Created on Jan 8, 2015

@author: Susan
'''

import os
import subprocess


if __name__ == '__main__':
    myDirectory = "Assignment4"
    myAssignment = "CA04"
    os.chdir("F:\\git\\6700Fall14\\Assignment4\\submissions\\xu--yangfan-late_3132310_47261211_yzx0018\\softwareProcess\\.git")
    p=subprocess.Popen(["git","log","-p","-m","--reverse","--pretty=format:\"%s\""],stdout=subprocess.PIPE)
    outFile = open("f:\\git\\6700Fall14\\"+myDirectory+"\\xu--yangfan-late_3132310_47261211_yzx0018Log", "w")
    for line in p.stdout.readlines():
        outFile.write(line)
    outFile.close()