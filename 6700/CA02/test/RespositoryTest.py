'''
Created on Sep 7, 2014

@author: Brenden
'''
import unittest
import CA02.prod.Component as Component
import CA02.prod.Repository as Repository

class TestRepository(unittest.TestCase):

# Constructor
    #100_0xx ... happy 
    def test100_010_ShouldConstructRepositoryExplicitCapacity(self):
        self.assertIsInstance(Repository.Repository(capacity=100), Repository.Repository)
        
    def test100_020_ShouldConstructRepositoryDefaultCapacity(self):
        self.assertIsInstance(Repository.Repository(), Repository.Repository)
        
    #100_9xx ... sad path
    def test100_910_ShouldRaiseExceptionOnNonIntCapacity(self):
        expectedString = "Repository.__init__:"
        try:
            Repository.Repository("a")                                                
            self.fail("exception was not raised")                    
        except ValueError as raisedException:                                           
            diagnosticString = raisedException.args[0]                                   
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)]) 
        except:
            self.fail("incorrect exception was raised") 
    
    def test100_920_ShouldRaiseExceptionOnInvalidCapacity(self):
        expectedString = "Repository.__init__:"
        try:
            Repository.Repository(capacity=0)                                                
            self.fail("exception was not raised")                    
        except ValueError as raisedException:                                           
            diagnosticString = raisedException.args[0]                                   
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)]) 
        except:
            self.fail("incorrect exception was raised")     

    
# addComponent
    #200_0xx ... happy path
    def test200_010_shouldAddComponent(self):
        maxCapacity = 2
        theRepository = Repository.Repository(maxCapacity)
        for i in range(maxCapacity):
            self.assertEquals(i+1, theRepository.addComponent(Component.Component("C"+str(i), i+1, i+1)))
            
    def test200_020_shouldAddComponentPastCapacity(self):
        maxCapacity = 2
        theRepository = Repository.Repository(maxCapacity)
        for i in range(maxCapacity):
            theRepository.addComponent(Component.Component("C"+str(i), i+1, i+1))
            
        self.assertEquals(maxCapacity, theRepository.addComponent(Component.Component("overflow", 1, 10)))
        
    def test200_020_shouldDeleteOldestPastCapacity(self):
        maxCapacity = 2
        theRepository = Repository.Repository(maxCapacity)
        # Add maxCapacity+1 components
        # Ensure the first one has a zero method count, all others have non-zero method count
        # We infer that the first component -- the only component with a non-zero method count -- has
        # been deleted if validCount() == 2
        for i in range(maxCapacity+1):
            theRepository.addComponent(Component.Component("C"+str(i), i, i+1))
        self.assertEquals(2, theRepository.validCount())
        
    def test200_910_shouldRaiseExceptionIfComponentMissing(self):
        #AMBexpectedString = "Repository.addComponent:  "
        expectedString = "Repository.addComponent:"
        theRepository = Repository.Repository()
        try:                                             
            theRepository.addComponent()
            self.fail("exception was not raised")                    
        except ValueError as raisedException:                                           
            diagnosticString = raisedException.args[0]                                   
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)]) 
        except:
            self.fail("incorrect exception was raised")  
               
    def test200_920_shouldRaiseExceptionOnDuplicateComponent(self):
        expectedString = "Repository.addComponent:"
        theRepository = Repository.Repository()
        component = Component.Component("C1", 5, 100)
        duplicate = Component.Component("C1", 5, 100)
        theRepository.addComponent(component)
        try:
            theRepository.addComponent(duplicate)
            self.fail("exception was not raised")                    
        except ValueError as raisedException:                                           
            diagnosticString = raisedException.args[0]                                   
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)]) 
        except:
            self.fail("incorrect exception was raised")          
         
# count
    #300_0xx ... happy path
    def test300_010_shouldReturnInt(self):
        maxCapacity = 10
        theRepository = Repository.Repository(maxCapacity)
        for i in range(maxCapacity):
            theRepository.addComponent(Component.Component("C"+str(i), i+1, i+1))
        self.assertIsInstance(theRepository.count(), int)
            
        self.assertEquals(maxCapacity, theRepository.addComponent(Component.Component("overflow", 1, 10)))    
    def test300_020_shouldReturnCount(self):
        maxCapacity = 10
        theRepository = Repository.Repository(maxCapacity)
        for i in range(maxCapacity):
            theRepository.addComponent(Component.Component("C"+str(i), i+1, i+1))
            self.assertEqual(i+1, theRepository.count())
        self.assertEquals(maxCapacity, theRepository.addComponent(Component.Component("overflow", 1, 10)))
        
        
# validCount
    #400_0xx ... happy path
    def test400_010_shouldReturnInt(self):
        maxCapacity = 10
        theRepository = Repository.Repository(maxCapacity)
        for i in range(maxCapacity):
            theRepository.addComponent(Component.Component("C"+str(i), i+1, i+1))
        self.assertIsInstance(theRepository.validCount(), int)  
         
    def test500_010_shouldReturnValidCount(self):
        maxCapacity = 10
        theRepository = Repository.Repository(maxCapacity)
        for i in range(maxCapacity):
            theRepository.addComponent(Component.Component("C"+str(i), 0, i+1))
            self.assertEqual(0, theRepository.validCount())
        
# deteremineRelativeSize
    #600_0xx . . . happy path
    def test600_010_shouldReturnIntList(self):
        maxCapacity = 10
        theRepository = Repository.Repository(maxCapacity)
        methodCounts = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        locCounts = [42, 19, 58, 60, 70, 82, 57, 89, 80, 128]
        for i in range(maxCapacity):
            theRepository.addComponent(Component.Component("C"+str(i), methodCounts[i], locCounts[i]))
        listOfSizes = theRepository.determineRelativeSizes()
        self.assertIsInstance(listOfSizes, list)
        for size in listOfSizes:
            self.assertIsInstance(size, int)
        
    def test600_020_shouldReturnSizeList(self):
        # test set:
        #name methods LOC   ln(loc/methods)
        #C0    0    42    NA
        #C1    1    19    2.944438979
        #C2    2    58    3.36729583
        #C3    3    60    2.995732274
        #C4    4    70    2.862200881
        #C5    5    82    2.797281335
        #C6    6    57    2.251291799
        #C7    7    89    2.542726221
        #C8    8    80    2.302585093
        #C9    9    128    2.654805687
        #          avg = 2.746484233
        #          stdev = 0.352645834
        #  This yields [8, 11, 16, 23, 32]
        maxCapacity = 10
        theRepository = Repository.Repository(maxCapacity)
        methodCounts = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        locCounts = [42, 19, 58, 60, 70, 82, 57, 89, 80, 128]
        for i in range(maxCapacity):
            theRepository.addComponent(Component.Component("C"+str(i), methodCounts[i], locCounts[i]))
        self.assertListEqual([8, 11, 16, 23, 32], theRepository.determineRelativeSizes())        
        
    def test600_030_shouldReturnSizeList(self):
        # test set:
        #name methods LOC   ln(loc/methods)
        #C0    0    42    NA
        #C1    1    19    2.944438979
        #C2    2    58    3.36729583
        #C3    3    60    2.995732274
        #C4    4    70    2.862200881
        #C5    5    82    2.797281335
        #C6    6    57    2.251291799
        #C7    7    89    2.542726221
        #C8    8    80    2.302585093
        #C9    9    128    2.654805687
        #          avg = 2.746484233
        #          stdev = 0.352645834
        #  This yields [8, 11, 16, 23, 32]
        maxCapacity = 4
        theRepository = Repository.Repository(maxCapacity)
        methodCounts = [1, 4, 7, 5]
        locCounts = [76, 116, 113, 103]
        for i in range(maxCapacity):
            theRepository.addComponent(Component.Component("C"+str(i), methodCounts[i], locCounts[i]))
        self.assertListEqual([8, 15, 30, 58, 115], theRepository.determineRelativeSizes())        
        
    #600_9xx . . . sad path
    def test600_910_shouldRaiseExceptionOnSmallCapacity(self):  
        expectedString = "Repository.determineRelativeSizes:" 
        maxCapacity = 100
        theRepository = Repository.Repository(maxCapacity)
        theRepository.addComponent(Component.Component("LoneComponent", 1, 10))
        try:
            theRepository.determineRelativeSizes()                                         
            self.fail("exception was not raised")                    
        except ValueError as raisedException:                                           
            diagnosticString = raisedException.args[0]                                   
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)]) 
        except:
            self.fail("incorrect exception was raised") 
            
    def test600_920_shouldRaiseExceptionOnTooFewValidComponents(self):  
        expectedString = "Repository.determineRelativeSizes:" 
        maxCapacity = 100
        theRepository = Repository.Repository(maxCapacity)
        theRepository.addComponent(Component.Component("NonZero", 1, 10))
        theRepository.addComponent(Component.Component("Zero", 0, 10))
        try:
            theRepository.determineRelativeSizes()                                         
            self.fail("exception was not raised")                    
        except ValueError as raisedException:                                           
            diagnosticString = raisedException.args[0]                                   
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)]) 
        except:
            self.fail("incorrect exception was raised") 
            
#getRelativeSize
    def test700_010_shouldReturnRelativeSizeOfComponent(self):
        component1 = Component.Component(name="Component01", methodCount=1, locCount=76)
        component2 = Component.Component(name="Component02", locCount= 116, methodCount=4)
        component3 = Component.Component("Component03", 7, locCount = 113)
        component4 = Component.Component("Component04", 5, 103)
        component5 = Component.Component("Component05", 0, 10)
        theRepository = Repository.Repository()
        theRepository.addComponent(component1)
        theRepository.addComponent(component2)
        theRepository.addComponent(component3)
        theRepository.addComponent(component4)
        theRepository.addComponent(component5)
        self.assertEquals("L", theRepository.getRelativeSize(component1))
        
    def test700_910_shouldRaiseExceptionWhenComponentParameterMissing(self):
        R1 = Repository.Repository()
        expectedString = "Repository.getRelativeSize:" 
        try:
            R1.getRelativeSize()
            self.fail("exception was not raised")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]                                   
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
            self.fail("incorrect exception was raised")
            
    def test700_920_shouldRaiseExceptionWhenComponentHasNoMethods(self):
        R1 = Repository.Repository()
        C1 = Component.Component("C1", 0, 1)
        R1.addComponent(C1)
        expectedString = "Repository.getRelativeSize:" 
        try:
            R1.getRelativeSize(C1)
            self.fail("exception was not raised")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]                                   
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
            self.fail("incorrect exception was raised")        
            
    def test700_930_shouldRaiseExceptionWhenRepositoryHasInsufficientData(self):
        R1 = Repository.Repository()
        C1 = Component.Component("C1", 5, 100)
        R1.addComponent(C1)
        expectedString = "Repository.getRelativeSize:" 
        try:
            R1.getRelativeSize(C1)
            self.fail("exception was not raised")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]                                   
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
            self.fail("incorrect exception was raised")
            
#estimateByRelativeSize
    def test800_010_shouldReturnComponentInstanceWithEstimatedLOC(self):
        component1 = Component.Component(name="Component01", methodCount=1, locCount=76)
        component2 = Component.Component(name="Component02", locCount= 116, methodCount=4)
        component3 = Component.Component("Component03", 7, locCount = 113)
        component4 = Component.Component("Component04", 5, 103)
        component5 = Component.Component("Component05", 0, 10)
        theRepository = Repository.Repository()
        theRepository.addComponent(component1)
        theRepository.addComponent(component2)
        theRepository.addComponent(component3)
        theRepository.addComponent(component4)
        theRepository.addComponent(component5)
        component6 = theRepository.estimateByRelativeSize("Component06", 5, "S")
        self.assertTrue(isinstance(component6, Component.Component))
        self.assertEquals(component6.getName(), "Component06")
        self.assertEquals(component6.getMethodCount(), 5)
        self.assertEquals(component6.getLocCount(), 75)
        self.assertEquals(component6.getRelativeSize(), "S")
        
    def test800_020_shouldReturnComponentWhenSizeParameterMissing(self):
        component1 = Component.Component(name="Component01", methodCount=1, locCount=76)
        component2 = Component.Component(name="Component02", locCount= 116, methodCount=4)
        component3 = Component.Component("Component03", 7, locCount = 113)
        component4 = Component.Component("Component04", 5, 103)
        component5 = Component.Component("Component05", 0, 10)
        theRepository = Repository.Repository()
        theRepository.addComponent(component1)
        theRepository.addComponent(component2)
        theRepository.addComponent(component3)
        theRepository.addComponent(component4)
        theRepository.addComponent(component5)
        component6 = theRepository.estimateByRelativeSize("Component06", 5)
        self.assertTrue(isinstance(component6, Component.Component))
        self.assertEquals(component6.getRelativeSize(), "M")
        
    def test800_910_shouldThrowExceptionIfNameNotString(self):
        R1 = Repository.Repository()
        C1 = Component.Component("C1", 5, 100)
        C2 = Component.Component("C2", 3, 20)
        R1.addComponent(C1)
        R1.addComponent(C2)
        
        expectedString = "Repository.estimateRelativeSize:" 
        try:
            R1.estimateByRelativeSize(0, 6, "L")
            self.fail("exception was not raised")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]                                   
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
            self.fail("incorrect exception was raised")
            
    def test800_920_shouldThrowExceptionIfNameEmpty(self):
        R1 = Repository.Repository()
        C1 = Component.Component("C1", 5, 100)
        C2 = Component.Component("C2", 3, 20)
        R1.addComponent(C1)
        R1.addComponent(C2)
        
        expectedString = "Repository.estimateRelativeSize:" 
        try:
            R1.estimateByRelativeSize("", 6, "L")
            self.fail("exception was not raised")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]                                   
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
            self.fail("incorrect exception was raised")
            
    def test800_930_shouldThrowExceptionIfMethodCountLessThanOne(self):
        R1 = Repository.Repository()
        C1 = Component.Component("C1", 5, 100)
        C2 = Component.Component("C2", 3, 20)
        R1.addComponent(C1)
        R1.addComponent(C2)
        
        expectedString = "Repository.estimateRelativeSize:" 
        try:
            R1.estimateByRelativeSize("C3", 0, "L")
            self.fail("exception was not raised")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]                                   
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
            self.fail("incorrect exception was raised")     
            
    def test800_940_shouldThrowExceptionIfMethodCountIsNotAnInteger(self):
        R1 = Repository.Repository()
        C1 = Component.Component("C1", 5, 100)
        C2 = Component.Component("C2", 3, 20)
        R1.addComponent(C1)
        R1.addComponent(C2)
        
        expectedString = "Repository.estimateRelativeSize:" 
        try:
            R1.estimateByRelativeSize("C3", "1", "L")
            self.fail("exception was not raised")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]                                   
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
            self.fail("incorrect exception was raised")
            
    def test800_950_shouldThrowExceptionIfNameIsDuplicate(self):
        R1 = Repository.Repository()
        C1 = Component.Component("C1", 5, 100)
        C2 = Component.Component("C2", 3, 20)
        R1.addComponent(C1)
        R1.addComponent(C2)
        
        expectedString = "Repository.estimateRelativeSize:" 
        try:
            R1.estimateByRelativeSize("C1", "1", "L")
            self.fail("exception was not raised")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]                                   
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
            self.fail("incorrect exception was raised")   
            
    def test800_960_shouldRaiseExceptionWhenRepositoryHasInsufficientData(self):
        R1 = Repository.Repository()
        C1 = Component.Component("C1", 5, 100)
        R1.addComponent(C1)
        expectedString = "Repository.getRelativeSize:" 
        try:
            R1.getRelativeSize(C1)
            self.fail("exception was not raised")
        except ValueError as raisedException:
            diagnosticString = raisedException.args[0]                                   
            self.assertEquals(expectedString, diagnosticString[0:len(expectedString)])
        except:
            self.fail("incorrect exception was raised")    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()