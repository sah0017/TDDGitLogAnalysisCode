'''
Created on Sep 17, 2014

@author: susanha
'''
import printResults

if __name__ == '__main__':
    fileName = "fleming--joseph-late_470350_44914669_jpf0005Log"
    myResults = printResults.Results()
    avgLinesPerCommit, avgTransPerCommit = myResults.printResults(fileName)
    print fileName, avgLinesPerCommit, avgTransPerCommit
