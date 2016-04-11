'''
Created on Sep 9, 2014

@author: Brenden
'''
from __builtin__ import str

class Component:
    
    def __init__(self, name=None, methodCount=None, locCount=None):
        
        if name==None or methodCount==None or locCount==None:
            raise ValueError('Component.__init__:  Missing one or more parameters')
        
        elif type(name) is not str:
            raise ValueError('Component.__init__:  Name needs to be a string')
        
        elif type(methodCount) is not int:
            raise ValueError('Component.__init__:  methodCount needs to be an int')
        
        elif type(locCount) is not int:
            raise ValueError('Component.__init__:  locCount needs to be an int')
        
        elif methodCount < 0 or locCount <= 0 or len(name) <= 0:
            raise ValueError('Component.__init__:  Invalid parameters values')
        
        else:
            self.name = name
            self.methodCount = methodCount
            self.locCount = locCount
            self.relativeSize = None

    def getName(self):
        return self.name
        
    def getMethodCount(self):
        return self.methodCount
        
    def getLocCount(self):
        return self.locCount 
    
    def setRelativeSize(self, relativeSize="M"):
        if type(relativeSize) is not str:
            raise ValueError('Component.setRelativeSize:  Parameter must be string type')   
             
        relativeSize = relativeSize.upper()
        if relativeSize not in ["VS", "S", "M", "L", "VL"]:
            raise ValueError('Component.setRelativeSize:  Invalid parameter value')
        
        self.relativeSize = relativeSize
        return self.relativeSize
    
    def getRelativeSize(self):
        if self.relativeSize==None:
            raise ValueError('Component.getRelativeSize:  Relative size not set for this component')
        
        return self.relativeSize
        