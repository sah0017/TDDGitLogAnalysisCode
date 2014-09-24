'''
Created on Sep 17, 2014

@author: susanha
'''
import printResults

if __name__ == '__main__':
    fileName = "antley--matthew_1247150_44878954_mra0016Log"
    myResults = printResults.Results()
    nbrCommits, avgLinesPerCommit, avgTransPerCommit = myResults.printResults(fileName)
    print fileName, nbrCommits, avgLinesPerCommit, avgTransPerCommit
