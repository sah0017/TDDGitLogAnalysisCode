'''
Created on May 24, 2017

@author: susanha
'''

import Assignment
import jsonpickle
import FileHandler
import os
import ConfigParser



class Recommender(object):

    def __init__(self):
        myConfig = ConfigParser.SafeConfigParser()
        myConfig.read("TDDanalysis.cfg")

        for key, val in myConfig.items("Recommendations"):
            self.RecommendDict[key] = time.strptime(val,"%Y, %m, %d")

    def provideRecommendations(self):
        pass



