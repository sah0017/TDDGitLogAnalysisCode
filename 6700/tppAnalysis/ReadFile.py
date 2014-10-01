'''
Created on Jul 10, 2014

@author: susanha
'''

if __name__ == '__main__':
    gitFile = open("C:\\Users\\susanha\\git\\6700test\\revLogFile")
    line = gitFile.readline()
    if line.find("I n i t i a l") > -1:
        print line
    ##for line in gitFile:
    ##    print line
