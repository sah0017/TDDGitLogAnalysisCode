'''
Created on Sep 17, 2014

@author: susanha
'''
import AnalyzeAGitFileAndCreategitoutFile

if __name__ == '__main__':
    #  antley--matthew_1247150_45465189_mra0016Log
    #  romanowski--brenden_481945_45480789_btr0005Log
    #  bryant--james_2270195_45451066_jab0091Log
    fileName = "szw0069Log"
    myResults = AnalyzeAGitFileAndCreategitoutFile.Results("CA03")
    nbrCommits, avgLinesPerCommit, avgTransPerCommit, ratio, allDeletedLines = myResults.printResults("g:\\git\\6700Fall15\\CA03",fileName)
    print fileName, nbrCommits, avgLinesPerCommit, avgTransPerCommit, ratio, allDeletedLines
