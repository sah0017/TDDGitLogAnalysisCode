'''
Created on Jul 28, 2014

@author: susanha
'''

import re
import math

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
        myString = "myValue=myValue + 1"
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
        myObj = re.search(r'=',myString.strip())  ## looking for a number or [] or " or '
        if myObj:
            if (re.search(r'==',myString)):
                print 'evaluation'
            else:
                print 'assignment'

        else:
            print 'not found'
            
    def newMethod(self):
        math.ceil(2.55)
        
        

            