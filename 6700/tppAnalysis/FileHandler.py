'''
Created on May 15, 2017

@author: susanha
'''

import codecs

class FileHandler(object):

    def __init__(self):
        pass

    def open_file(self, filename):
        self.file = codecs.open(filename)

    def readNextLine(self):
        try:
            line = self.file.next()
            return line
        except StopIteration as e:
            return False

    def close_file(self):
        self.file.close()
