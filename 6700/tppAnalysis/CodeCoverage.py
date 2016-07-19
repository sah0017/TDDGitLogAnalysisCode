'''
Created on Jul 1, 2016

@author: susanha
'''
import sys, os, re, unittest, coverage
from unittest.runner import TextTestRunner
from coverage.misc import CoverageException
import time, traceback
from contextlib import contextmanager
from py._iniconfig import SectionWrapper
import ConfigParser

errorDict = {-1:"Coverage Exception",
             -2:"Run Error",
             -3:"Import Error/Didn't get to student's tests"}
@contextmanager
def redirect_stdout(new_target):
    old_target, sys.stdout = sys.stdout, new_target
    try:
        yield new_target
    finally:
        sys.stdout = old_target

class CodeCoverage(object):
    def __init__(self):
        '''
        Constructor
        '''
         
        #myConfig = ConfigParser.ConfigParser() 
        #myConfig.read("analysis.cfg")
        #self.root = myConfig.get("Location","Root")
        self.assignment = ""
        self.dataFile = ""
        
    
           

    def analyzeCodeCoverage(self, root, assignment):
        try:
            submissionPath = ""
            cov = coverage.Coverage(data_file=root+".cvg",include=root + "\\*.py", branch=True )
            nameSplit = root.split("\\")
            fileName = nameSplit[5]
            for i in range(0,3):
                submissionPath = submissionPath + nameSplit[i] +"\\"
            with open(os.path.join(submissionPath + assignment + ".result"), "a+") as resultoutFile:
                resultoutFile.write("\n\rStudent submission and path:  " + root + "\n\r")
            studentName = fileName.split("_")
            testpath = os.path.join(root + "\\test") 
            prodpath = os.path.join(root + "\\prod")  
            print "testpath " + testpath
            print "prodpath " + prodpath
            sys.path.insert(0,root)
            sys.path.insert(0,prodpath)
            sys.path.insert(0,testpath)
            testfiles = os.listdir(testpath)                               
            prodfiles = os.listdir(prodpath)  
            os.chdir(testpath)  
            print "sys.path " + sys.path[0]                           
            myTestLoader = unittest.TestLoader()  
            test = re.compile(r"\b.py\b", re.IGNORECASE)          
            testfiles = filter(test.search, testfiles)                     
            prodfiles = filter(test.search, prodfiles)                     
            filenameToModuleName = lambda f: os.path.splitext(f)[0]
            moduleTestNames = map(filenameToModuleName, testfiles)   
            #moduleProdNames = map(filenameToModuleName, prodfiles)   
            cov.start()
            '''
            from importlib import import_module
            '''
            with open(os.path.join(submissionPath + assignment + ".result"), "a+") as resultoutFile:
                resultoutFile.write("Test Names\n\r")
            for mtn in moduleTestNames:
                print mtn
                with open(os.path.join(submissionPath + assignment + ".result"), "a+") as resultoutFile:
                    resultoutFile.write(mtn + "\r")
            
            
            load = myTestLoader.loadTestsFromNames(moduleTestNames)  
            print load.countTestCases()
        except Exception as e:
            with open(os.path.join(submissionPath + assignment + ".result"), "a+") as resultoutFile:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback,file=resultoutFile)
            return -3, studentName[0]
        result = False
        result = TextTestRunner().run(load)
        time.sleep(1)
        with open(os.path.join(submissionPath + assignment + ".result"), "a+") as resultoutFile:
            resultoutFile.write("Number of tests run:  " + str(result.testsRun) + "\n\r")
            if not result.wasSuccessful():
                resultoutFile.write("Content of TextTestRunner result.failures\r")
                for failedTestCase, failure in result.failures:
                    resultoutFile.write(str(failedTestCase) + failure + "\n\r")
        '''
        f, s, excluded, missing, m = cov.analysis2('g:\\git\\6700Spring16\\CA05\\submissions\\danieljames_1246453_74826857_jhd0008\\softwareProcess\\SoftwareProcess\\Assignment\\prod\\Fix.py')
        print "file name:  " + f, "\n\rline numbers of executable statements:  " + str(s).strip('[]'), "\n\rline numbers of excluded statements:  "+str(excluded).strip('[]'), "\n\rline numbers missing from execution:  "+str(missing).strip('[]'), "\n\rstring with missing line numbers:  "+m
         
        
        for fn in moduleTestNames:
            if fn != "__init__.py":
                f, s, excluded, missing, m = cov.analysis2('g:\\git\\6700Spring16\\CA05\\submissions\\danieljames_1246453_74826857_jhd0008\\softwareProcess\\SoftwareProcess\\Assignment\\test\\' + fn + '.py')
                print "file name:  " + f, "\n\rline numbers of executable statements:  " + str(s).strip('[]'), "\n\rline numbers of excluded statements:  "+str(excluded).strip('[]'), "\n\rline numbers missing from execution:  "+str(missing).strip('[]'), "\n\rstring with missing line numbers:  "+m
        for fn in prodfiles:
            if fn != "__init__.py":
                f, s, excluded, missing, m = cov.analysis2('g:\\git\\6700Spring16\\CA05\\submissions\\danieljames_1246453_74826857_jhd0008\\softwareProcess\\SoftwareProcess\\Assignment\\prod\\' + fn)
                print "file name:  " + f, "\n\rline numbers of executable statements:  " + str(s).strip('[]'), "\n\rline numbers of excluded statements:  "+str(excluded).strip('[]'), "\n\rline numbers missing from execution:  "+str(missing).strip('[]'), "\n\rstring with missing line numbers:  "+m
        '''
        cov.stop()
        cov.save()
            
        if result.wasSuccessful():
            try:
                cov.html_report(directory=submissionPath)
                with open(os.path.join(submissionPath + assignment + ".result"), "a+") as f, redirect_stdout(f):
                    pctg = cov.report()
                print pctg
                #raw_input("Continue (success)?")
                return pctg, studentName[0]
            except CoverageException:
                print "CoverageException testpath" + testpath 
                with open(os.path.join(submissionPath + assignment + ".result"), "a+") as resultoutFile:
                    resultoutFile.write("CoverageException \n\r")
                #raw_input("Continue (CoverageException)?")
                return -1, studentName[0]
        else:
            print "Result not successful testpath" + testpath 
            with open(os.path.join(submissionPath + assignment + ".result"), "a+") as resultoutFile:
                resultoutFile.write("Result not successful \n\r")
            
            #raw_input("Continue (result not successful)?")
            return -2, studentName[0]
        

if __name__ == '__main__':
    totalArgs = len(sys.argv)
    args = str(sys.argv)
    
    
    myCodeCoverage = CodeCoverage()
    '''
    with open("g:\\git\\6700Spring16\\"+myCodeCoverage.assignment+"\\"+myCodeCoverage.assignment+".cvgrpt", "w") as outFile :
        outFile.write("Module Name\t\tCode Coverage percentage\n\r")
    with open("g:\\git\\6700Spring16\\"+myCodeCoverage.assignment+"\\"+myCodeCoverage.assignment+".result", "w") as resultoutFile:
        resultoutFile.write("Run date/time:  " + time.strftime("%a, %d %b %Y %H:%M:%S")+"\n\r")
    '''
    if totalArgs > 1:
        dataFile = str(sys.argv[1])
        myCodeCoverage.assignment = str(sys.argv[2])
    else:
        #dataFile = "g:\\git\\6700Spring16\\CA03\\submissions\\yanyufei_late_3331231_73091650_yzy0050CA03\\SoftwareProcess\\SoftwareProcess\\Assignment\\"
        dataFile = "g:\\git\\6700Spring16\\CA05\\submissions\\bakerthomas_late_1313011_74933289_thb0008CA05\\Software_Process03\\Software_Process03\\Assignment\\"
        myCodeCoverage.assignment = "CA05"
    print ("Datafile location is : %s" % dataFile)
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage(dataFile,myCodeCoverage.assignment)
    '''
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\bakerthomas_late_1313011_71435710_thb0008CA02\\Software_Process\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\brownejonathan_late_1743863_71441243_JJB0031CA02\\softwareProcess\\jjb0031\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\carpenterjames_late_479328_71685202_jrc0040CA02\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\carrolljohn_late_648283_71440609_jcc0044CA02\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\carterjoshua_late_477776_71350122_JPC0017_CA02\\AssignmentCA02\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\chadasaicharanreddy_3196713_71343042_SZC0081CA02\\SZC0081CA02\\CA02\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\coxjames_3059804_71348157_softwareProcess_300316\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\coxjames_3059804_71348157_softwareProcess_300316\\softwareProcess\\SoftwareProcess\\CA02\\","CA02")
    
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\coxjames_late_3059804_73753063_softwareProcess_300316-1\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\coxjames_late_3059804_73753063_softwareProcess_300316-1\\softwareProcess\\SoftwareProcess\\CA02\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\danieljames_1246453_71344063_jhd0008CA02\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\edgarbethany_445804_71343532_bke0002-5\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\fernandezbrandon_late_480792_71808865_bmf0008ca02\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\fernandezbrandon_late_480792_71808865_bmf0008ca02\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\fordbenjamin_1246142_71238474_bkf0003CA02-1\\SoftwareProcess\\SoftwareProcess\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\fordbenjamin_1246142_71238474_bkf0003CA02-1\\SoftwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\gastonjoshua_late_1257396_71348265_jcg0031ca02\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\griffithsueanne_2169181_71345788_sng0005_CA02\\softwareProcess\\sng0005\\CA01\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\griffithsueanne_2169181_71345788_sng0005_CA02\\softwareProcess\\sng0005\\CA02\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\griffithsueanne_2169181_71345788_sng0005_CA02\\softwareProcess\\TCurve_Griffith\\FA03\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\hallmichael_late_2242176_71422437_Mlh0045-3\\SoftwareProcessCA02\\AssignmentCA02\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\heckenbachmike_495569_71348049_mah0036CA02\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\hesterwilliam_1246183_71342600_weh0008-3\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\hoovertyler_1313107_71336105_tkh0006-2\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\jariwalaabhishekvirendrabhai_3353850_71346014_avj0003CA02\\SoftwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\johnsonblake_1245904_71238871_brj0003-1\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\johnsoncollin_1246513_71343098_cjj0008-4\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\jonesconnor_471160_71346366_caj0006-5\\SoftwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\jonesconnor_471160_71346366_caj0006-5\\__MACOSX\\SoftwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\joygarrett_2076264_71333906_gdj0004-3\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\lantianhang_late_3319007_72743736_TZL0033CA02\\SoftwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\liuguanting_late_3334401_71531175_gzl0024CA02\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\lixiao_3161403_71149243_xzl0040CA02-2\\SoftwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\macdonaldallison_late_3122825_71441848_amm0086_CA02\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\malanxin_3113732_71348186_lmm0033.zip\\SoftwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\mcduffieglenn_1245934_71345232_gsm0006CA02\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\mulkinjonathan_late_1285176_71442580_jpm0027_CA02\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\murphyolivia_1246266_71241341_onm0002CA02\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\okeefecasey_1284976_71346148_cwo0002-1\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\openshawnicholas_late_648223_71348339_CA02\\CA02\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\pearcemichael_3068727_71348251_mtp0013CA02-1\\StarNavigation\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\pennbridges_1246279_71338894_bjp0008CA02\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\pickensstacy_1245964_71327045_sep0020-4\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\puttaravinder_3353861_71347475_rzp0039CA02\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\regelmanshelby_476126_71348148_snr0006CA02\\src\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\regelmanshelby_late_476126_71441966_snr0006CA02-1\\src\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\reynoldslucy_1254103_71346156_lcr0011CA02\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\rogersthomas_1246860_71327047_tmr0012-1\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\sanchezcesar_1740491_71345857_SoftwareProcess\\SoftwareProcess\\src\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\sanchezcesar_late_1740491_71441427_SoftwareProcess-1\\SoftwareProcess\\src\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\scottjacob_3126629_71348250_CA02_Jss0040\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\seayedward_648520_71341383_ers0007CA02\\SoftwareProcess\\SoftwareProcess\\CA02\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\seayedward_648520_71341383_ers0007CA02\\__MACOSX\\SoftwareProcess\\SoftwareProcess\\CA02\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\sivarajsunit_3354503_71345936_szs0144CA02\\SoftwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\sivarajsunit_3354503_71345936_szs0144CA02\\SoftwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\smithennis_466292_71339787_ebs0009CA02\\SoftwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\smithneal_464502_71343739_nrs0002CA02\\SoftwareProcess\\Assignment\\","CA02")
    
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\sultananawrin_3205338_71344358_nzs0034CA02-1\\SoftwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\tangchengyu_late_3324928_71348629_czt0026CA02-1\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\towlesgeorge_late_3016544_71348306_softwareProcess_300316\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\weisesamuel_1246642_71345968_saw0025-3\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\whaleyjay_late_1255621_71348460_jpw0032-CA02\\softwareProcess\\CA02 - Altitude Correction\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\whaleyjay_late_1255621_71348460_jpw0032-CA02\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\williamsonalexandria_1246651_71344417_amw0042-3\\softwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\wilsonbrandon_late_3067816_72403188_bsw0015_CA02\\SoftwareProcess\\CA02\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\woodsjeremy_3118166_71336647_jbw0033CA02-1\\SoftwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\yanyufei_3331231_71345972_yzy0050CA02\\SoftwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\yanyufei_3331231_71345972_yzy0050CA02\\__MACOSX\\SoftwareProcess\\SoftwareProcess\\Assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\zhangchaowei_3357850_71348020_czz0032CA02\\softwareProcess\\assignment\\","CA02")
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage("g:\\git\\6700Spring16\\CA02\\submissions\\zhuqi_late_3232019_73078080_CA02\\CA02\\","CA02")
    
    '''
    print myPct, sName
    with open("g:\\git\\6700Spring16\\"+myCodeCoverage.assignment+"\\"+myCodeCoverage.assignment+".cvgrpt", "a+") as outFile:
        if myPct < 0:
            outFile.write("\n\r" + sName + "\t\t" + errorDict[myPct])
        else:
            outFile.write("\n\r" + sName + "\t\t" + format(myPct, ".2f"))
    

    