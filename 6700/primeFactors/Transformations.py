'''
Created on Jul 10, 2014

@author: susanha
'''

class Trans(object):
    '''
    classdocs
    '''
    NEWFILE = 0
    NULL = 1
    N2C = 2
    C2V = 3
    AComp = 4
    SF = 5
    VA = 6
    AC = 7
    I2W = 8
    REC = 9
    IT = 10
    AS = 11
    ACase = 12
    ConstOnly = -2
    transList = dict(NEWFILE=0, NULL=1, N2C=2, C2V=3, AComp=4,SF=5,VA=6,AC=7,I2W=8,REC=9,IT=10,AS=11,ACase=12)

    def __init__(self):
        '''
        Constructor
        '''

        
        