'''
Created on Aug 11, 2014

@author: susanha
'''



def fibonacci(value):
    
    if (value == 0):
        return 0
    if (value == 1):
        return 1
    return fibonacci(value - 1) + fibonacci(value - 2)    