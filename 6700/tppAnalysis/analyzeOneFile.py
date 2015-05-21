'''
Created on Sep 17, 2014

@author: susanha
'''
import printResults

if __name__ == '__main__':
    #  antley--matthew_1247150_45465189_mra0016Log
    #  romanowski--brenden_481945_45480789_btr0005Log
    #  bryant--james_2270195_45451066_jab0091Log
    fileName = "villarrubia--matthew_476477_47238656_mrv0003Log"
    myResults = printResults.Results("CA04")
    nbrCommits, avgLinesPerCommit, avgTransPerCommit, ratio, allDeletedLines = myResults.printResults("g:\\git\\6700Fall14\\Assignment4",fileName)
    print fileName, nbrCommits, avgLinesPerCommit, avgTransPerCommit, ratio, allDeletedLines
