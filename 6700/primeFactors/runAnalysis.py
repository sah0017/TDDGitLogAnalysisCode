'''
Created on Sep 12, 2014

@author: susanha
'''
import os
import printResults


if __name__ == '__main__':
    root = "c:\\Users\\susanha\\git\\6700Fall14\\Assignment1"
    dir = os.listdir(root)
    myResults = printResults.Results()
    for item in dir:
        #print item
        if os.path.isfile(os.path.join(root,item)):
            fileName, ext = os.path.splitext(item)
            if ext == "":
                myResults.printResults(fileName)
            print fileName, ext
'''
    for root, dir, files in os.walk("c:\\Users\\susanha\\git\\6700Fall14\\Assignment1\\submissions"):
        nameSplit = root.split("\\")
        if ".git" in root:
            if len(nameSplit) > 7:
                os.chdir("c:\\Users\\susanha\\git\\6700Fall14\\Assignment1\\submissions\\"+nameSplit[7]+"")
                print nameSplit[7]
        else:
            print "No git folder in " + root
        #print files
'''