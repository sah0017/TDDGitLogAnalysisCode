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
    VarOnly = -3
    WhileNoIf = -8
    transList = dict(NEWFILE=0, NULL=1, N2C=2, C2V=3, AComp=4,SF=5,VA=6,AC=7,I2W=8,REC=9,IT=10,AS=11,ACase=12)

    def __init__(self):
        '''
        Constructor
        '''
    def myName(self, transNbr):
        if transNbr == 0:
            return "New file"
        elif transNbr == 1:
            return "Null"
        elif transNbr == 2:
            return "Null to Constant"
        elif transNbr == 3:
            return "Constant to Variable"
        elif transNbr == 4:
            return "Add Computation"
        elif transNbr == 5:
            return "Split Flow"
        elif transNbr == 6:
            return "Variable to Array "
        elif transNbr == 7:
            return "Array to Container"
        elif transNbr == 8:
            return "If to While"
        elif transNbr == 9:
            return "Recurse"
        elif transNbr == 10:
            return "Iterate"
        elif transNbr == 11:
            return "Assign"
        elif transNbr == 12:
            return "Add Case"
        elif transNbr == -2:
            return "Straight to Constant"
        elif transNbr == -3:
            return "Straight to Variable"
        elif transNbr == -8:
            return "While with no If"
        


class NewFile(Trans):
    def myName(self):
        return "New File"
        