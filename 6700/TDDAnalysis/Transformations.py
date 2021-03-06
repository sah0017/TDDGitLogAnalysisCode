"""
Created on Jul 10, 2014

@author: susan hammond
"""


class Trans(object):
    """
    This class is used to define the transformations and anti-transformations without
    hard coding the information.
    """
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
    NA1 = -1
    ConstOnly = -2
    VarOnly = -3
    NA4 = -4
    NA5 = -5
    ArrayNoVar = -6
    NA7 = -7
    WhileNoIf = -8
    transList = {"NEWFILE":0, "NULL":1, "N2C":2, "C2V":3, "AComp":4,"SF":5,"VA":6,"AC":7,"I2W":8,
                 "REC":9,"IT":10,"AS":11,"ACase":12,"NA1":-1, "ConstOnly":-2, "VarOnly":-3, "NA4":-4,
                 "ArrayNoVar": -6, "WhileNoIf":-8}
    penaltyList = {-2:1, -3:2, -8:1}

    @classmethod
    def getTransValue(cls, transkey):
        return cls.transList[transkey]

    def getTransList(self):
        return self.transList

    def __init__(self):
        """
        Constructor
        """

    def getTransformationName(self, trans_nbr):
        if trans_nbr == 0:
            return "New file"
        elif trans_nbr == 1:
            return "Null"
        elif trans_nbr == 2:
            return "Null to Constant"
        elif trans_nbr == 3:
            return "Constant to Variable"
        elif trans_nbr == 4:
            return "Add Computation"
        elif trans_nbr == 5:
            return "Split Flow"
        elif trans_nbr == 6:
            return "Variable to Array "
        elif trans_nbr == 7:
            return "Array to Container"
        elif trans_nbr == 8:
            return "If to While"
        elif trans_nbr == 9:
            return "Recurse"
        elif trans_nbr == 10:
            return "Iterate"
        elif trans_nbr == 11:
            return "Assign"
        elif trans_nbr == 12:
            return "Add Case"
        elif trans_nbr == -2:
            return "Straight to Constant"
        elif trans_nbr == -3:
            return "Straight to Variable"
        elif trans_nbr == -6:
            return "Straight to Array"
        elif trans_nbr == -8:
            return "While with no If"
        else:
            return ""


class NewFile(Trans):
    def getTransformationName(self):
        return "New PyFile"
