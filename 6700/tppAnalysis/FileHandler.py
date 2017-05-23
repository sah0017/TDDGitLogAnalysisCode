'''
Created on May 15, 2017

@author: susanha
'''

import codecs

class FileHandler(object):

    def __init__(self):
        self.line = ''

    def open_file(self, filename):
        self.file = codecs.open(filename)

    def readNextLine(self):
        try:
            self.line = self.file.next()
            return self.line
        except StopIteration as e:
            return False

    def getCurrentLine(self):
        return self.line

    def close_file(self):
        self.file.close()
