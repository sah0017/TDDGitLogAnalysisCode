'''
Created on Jul 28, 2014

@author: susanha
'''
import importlib
import inspect
import re
import os
import io
import math
import codecs
import sys
from unittest import TestLoader, TextTestRunner
import pkgutil
import runpy  
from unittest.runner import TextTestResult
from pkgutil import ImpImporter
from modulefinder import ModuleFinder

class sandbox(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        ''' does this work for comment
        i think so '''
     
    def myMethod(self):
        finder = ModuleFinder()
        myDrive = "g:\\"
        mySrcPath = "git\\6700Spring16\\CA05\\submissions\\danieljames_1246453_74826857_jhd0008\\softwareProcess\\SoftwareProcess\\Assignment\\prod"
        myPath = "git\\6700Spring16\\CA05\\submissions\\danieljames_1246453_74826857_jhd0008\\softwareProcess\\SoftwareProcess\\Assignment\\test"
        #myPath = "git\\6700Spring16\\CA05\\submissions"
        scriptname = myDrive+myPath+'\\FixTest.py'
        with io.open(scriptname) as scriptfile:
            code = compile(scriptfile.readall(),scriptname,'exec')
        mod = importlib.import_module('FixTest',package="Assignment")
        print 'Inspect output:'
        for i in inspect.getmembers((mod, inspect.ismodule)):
            print i[0]
        for root, myDir, files in os.walk(myDrive + myPath):
            for myFile in files:
                print myFile
        sys.path.insert(0,os.path.join(myDrive+myPath))
        print sys.path
        finder.run_script(os.path.join(myDrive+mySrcPath+'\\Fix.py'))
        print 'Loaded modules:'
        for name, mod in finder.modules.iteritems():
            print '%s: ' % name,
            print ','.join(mod.globalnames.keys()[:3])
        runpy.run_path(os.path.join(myDrive,myPath,'FixTest.py'))
        __all__ = []
        module_name = None
        for loader, module_name, is_pkg in pkgutil.walk_packages("g:\\"):
            print 'in for loop'
            #__all__.append(module_name)
            #module = loader.find_module(module_name).load_module(module_name)
            print 'Found submodule %s ' % module_name
        print module_name
        
        '''
        src_data = pkgutil.get_data('Assignment.prod',"Fix.py")
        if src_data == None:
            print "No source data"
        else:
            print src_data
        #mod = loader.load_module(myDrive+myPath+"Fix.py")
        myString = "diff --git a/rtb0006/CA01/prod/__init__.pyc b/rtb0006/CA01/prod/__init__.pyc"
        testSuite = TestLoader().discover("g:\\git\\6700Spring16\\CA05\\submissions\\danieljames_1246453_74826857_jhd0008\\softwareProcess\\SoftwareProcess\\Assignment\\test", pattern="*.py")
        ImpImporter("g:\\git\\6700Spring16\\CA05\\submissions\\danieljames_1246453_74826857_jhd00085\\softwareProcess\\SoftwareProcess\\Assignment\\prod")
        print testSuite.countTestCases()
        for p in sys.path:
            print p
        
        result = TextTestRunner().run(testSuite)
        print result.testsRun
        '''
        '''
        d1 = run_module('g:\\git\\6700Spring16\\CA05\\submissions\\almohaishimoayad_3221348_74842094_mha0012CA05\\softwareProcess\\SoftwareProcess\\Assignment\\test\\FixTest.py')
        print 'Loaded modules:' % d1
        mySplit=myString.split(" ")
        myfirstcond = mySplit[0]
        mycond = mySplit[1]
        mysecondcond = mySplit[2]
        if mySplit[0].startswith("("):
            mySplit[0] = mySplit[0][1:]
            index = 1
            for phrase in mySplit:
                if phrase.find(")"):
                    mySplit[index] = phrase[0:len(phrase)-1]
                index = index + 1
        removeTrailingChars = re.search(r"[a-zA-Z0-9_^):]",mysecondcond)
        if removeTrailingChars:
            mysecondcond = removeTrailingChars.group(0)
        
            
        print mySplit
        
        myObj = re.search(r'\py.\b',myString.strip())  ## looking for a number or [] or " or '
        if myObj:
            print 'found'

        else:
            print 'not found'
        '''    
    def newMethod(self):
        line = "Thu Sep 27 10:11:20 2018 +0530"
        assignment = "CA02"
        print re.split("[-\+]", line)
        
    def testfileMethod(self):
        fileName = "c:\\Users\\susanha\\git\\6700Fall14\\testfile.txt"
        testFile = codecs.open(fileName, encoding='utf-8')
        
        for line in testFile:
            print line
            if (line.strip() == "Line 3"):
                length = len(line)
                print length, line
                testFile.seek(-(length+1),1)
        testFile.close()

if __name__ == '__main__':

    mySandbox = sandbox()
    mySandbox.newMethod()

