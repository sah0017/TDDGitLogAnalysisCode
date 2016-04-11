'''
Created on Sep 9, 2014

@author: Brenden
'''
import math
import CA02.prod.Component as Component

class Repository:

    def __init__(self, capacity=100):
        
        if type(capacity) is not int:
            raise ValueError('Repository.__init__:  Capacity needs to be an int')
        
        elif capacity <= 0:
            raise ValueError('Repository.__init__:  Capacity must be greater than 0')
        
        else:            
            self.capacity = capacity
            self.components = []
        
    def addComponent(self, componentIn=None):
        
        if componentIn is None:
            raise ValueError('Repository.addComponent:  Component parameter missing')
        
        for component in self.components:
            if component.getName() == componentIn.getName():
                raise ValueError('Repository.addComponent:  Duplicate component')
        
        if len(self.components) == self.capacity:
            self.components.pop(0)
        self.components.append(componentIn)
        return len(self.components)
        
    def count(self):
        return len(self.components)
    
    def validCount(self):
        count = 0
        for component in self.components:
            if component.getMethodCount() > 0:
                count = count + 1
        return count 
               
    def determineRelativeSizes(self): 
        if self.validCount() < 2:
            raise ValueError('Repository.determineRelativeSizes:  Component count must be at least 2')
        
        normalizedSizes = self.normalizeSize(self.components)
        avg = self.average(normalizedSizes)
        stdev = self.stdDev(normalizedSizes, avg)
        
        vs = int(math.ceil(math.exp(avg-2*stdev)))
        s = int(math.ceil(math.exp(avg-stdev)))
        m = int(math.ceil(math.exp(avg)))
        l = int(math.ceil(math.exp(avg+stdev)))
        vl = int(math.ceil(math.exp(avg+2*stdev)))
        return [vs,s,m,l,vl]
    
    def getRelativeSize(self, component=None):
        if component==None:
            raise ValueError('Repository.getRelativeSize:  Component parameter missing')
        elif component.getMethodCount() == 0:
            raise ValueError('Repository.getRelativeSize:  Component must have at least one method')
        elif self.validCount() < 2:
            raise ValueError('Repository.getRelativeSize:  Repository has insufficient data for operation')
        
        normalizedSizes = self.normalizeSize(self.components)
        avg = self.average(normalizedSizes)
        stdev = self.stdDev(normalizedSizes, avg)
        inputSize = component.getLocCount() / component.getMethodCount()
        
        vs = int(math.ceil(math.exp(avg-1.5*stdev)))
        s = int(math.ceil(math.exp(avg-0.5*stdev)))
        l = int(math.ceil(math.exp(avg+0.5*stdev)))
        vl = int(math.ceil(math.exp(avg+1.5*stdev)))
        
        if inputSize <= vs:
            return "VS"
        elif inputSize <= s:
            return "S"
        elif inputSize <= l:
            return "M"
        elif inputSize <= vl:
            return "L"
        else:
            return "VL"
        
    def estimateByRelativeSize(self, name, methodCount, size="M"):
        if type(name) is not str:
            raise ValueError('Repository.estimateRelativeSize:  Name must be a string')
        elif name == "":
            raise ValueError('Repository.estimateRelativeSize:  Name must be of length greater than 0')
        elif methodCount < 1:
            raise ValueError('Repository.estimateRelativeSize:  Method count must be greater than 0')
        elif type(methodCount) is not int:
            raise ValueError('Repository.estimateRelativeSize:  Method count must be an integer')
        
        if self.validCount() < 2:
            raise ValueError('Repository.determineRelativeSizes:  Component count must be at least 2')
        
        for component in self.components:
            if component.getName() == name:
                raise ValueError('Repository.addComponent:  Duplicate component') 
        
        size = size.upper()
        sizes = self.determineRelativeSizes()
        
        if size=="VS":
            loc = methodCount*sizes[0]
        elif size=="S":
            loc = methodCount*sizes[1]
        elif size=="M":
            loc = methodCount*sizes[2]
        elif size=="L":
            loc = methodCount*sizes[3]
        else:
            loc = methodCount*sizes[4]
            
        component = Component.Component(name, methodCount, loc)
        component.setRelativeSize(size)
        return component
        
    def normalizeSize(self, components):
        normalizedSizes = []
        for component in self.components:
            if component.getMethodCount() > 0:
                normal = component.getLocCount() / float(component.getMethodCount())
                normal = math.log(normal)
                normalizedSizes.append(normal)
        return normalizedSizes
    
    def average(self, values):
        avg = 0
        for value in values:
            avg = avg + value
        avg = avg / len(values)
        return avg
        
    def stdDev(self, values, avg):
        stdev = 0
        for value in values:
            difference = value - avg
            stdev += pow(difference,2)
        stdev = stdev/(len(values)-1)
        stdev = math.sqrt(stdev)
        return stdev   
        
    