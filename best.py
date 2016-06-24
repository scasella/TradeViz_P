
# coding: utf-8

# In[4]:

import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import urllib2
from multiprocessing import Pool as ThreadPool
import math
import cPickle
import os


# In[5]:

priceArr = []
patCollect = []
endingInd = []
patLen = 10
futureE = 10
quoteCollect = {}
bestArr = []

def percentChange(startPoint,currentPoint):
    try:
        x = ((float(currentPoint)-startPoint)/abs(startPoint))
        return x
    except:
        print(currentPoint, startPoint)
        return 0.00000000001

def loadPats():
    global priceArr

    priceArr = []
    with open(r"one.pickle", "rb") as input_file:
        e = cPickle.load(input_file)
        priceArr = e


def collectPats():
    global patCollect
    global endingInd
    patCollect = []
    endingInd = []
    for each in priceArr:
        tempCollect = []
        tempEnd = []
        sIndex = 0
        length = (len(each) - patLen - futureE)

        while sIndex < length:
            inc = 1
            tempPat = []
            while inc <= patLen:
                temp = percentChange(each[sIndex + inc -1], each[sIndex + inc])
                inc += 1
                tempPat.append(temp)
            tempCollect.append(tempPat)
            tempEnd.append(sIndex+patLen)
            sIndex += (patLen)
        patCollect.append(tempCollect)
        endingInd.append(tempEnd)

loadPats()
collectPats()


# In[6]:

def yahooLoad(val):
    tempArr = []
    string = ""
    string = 'http://ichart.finance.yahoo.com/table.csv?s={0}'.format(val)

    csv = urllib2.urlopen(string).readlines()
    #for bar in xrange(1,min(len(csv),500)):
    for bar in xrange(1,min(50,len(csv))):
        close = csv[bar].split(',')[6]
        tempArr.append(float(close))
    tempArr = tempArr[::-1]
    #quoteCollect[val] = tempArr
    return {val: tempArr}


def currentPat(curArr):
    global patLen
    curPat = []
    sliceLen = patLen
    curr = curArr[-(sliceLen+1):]
    while curr[-2] == curr[-1]:
        sliceLen += 1
        curr = curArr[-(sliceLen+1):]
    i = 0
    while i < patLen:
        temp = percentChange(curr[i], curr[i + 1])
        curPat.append(temp)
        i += 1
    return curPat


def sortPats(array):
    finalArr = []
    def getKey(tup):
        return tup[1]
    finalArr = sorted(array, key=getKey)
    return finalArr


# In[7]:

def matchPats(patCollect,endingInd,curPat):
    matchedPat = []
    matchedEndInd = []
    bestMatches = []
    for colInd,col in enumerate(patCollect):
        for rowInd,row in enumerate(col):
            mseCollect = []
            for ind,item in enumerate(row):
                mseTemp = abs(curPat[ind] - item)
                mseCollect.append(mseTemp)
            #mseAvg = np.average(weighting)
            mseAvg = np.average(mseCollect)
            bestMatches.append(([row,colInd,endingInd[colInd][rowInd]],mseAvg))
    test = sortPats(bestMatches)
    for item in test[:10]:
        matchedPat.append(item[0][0])
        matchedEndInd.append((item[0][1],item[0][2]))
    return matchedPat,matchedEndInd


# In[8]:

def plotting(matchedPat,matchedEndInd):
    global futureE
    futureAverages = []
    stDev = []
    futureLine = []
    futurePercent = []
    if len(matchedPat) > 1:
        for i in matchedPat:
            tempPercent = []
            refInd = matchedPat.index(i)
            endInd = matchedEndInd[refInd]
            col = endInd[0]
            outcomesZ = priceArr[col][endInd[1]:(endInd[1]+patLen)]
            futureLine.append(outcomesZ)
            for x in outcomesZ:
                change = percentChange(priceArr[col][endInd[1]],x)
                tempPercent.append(change)
            futurePercent.append(tempPercent)

        futureAverages = []

        for arrItemNum in range(len(futurePercent[0])):
            tempOutcomes = []
            for arr in futurePercent:
                tempOutcomes.append(arr[arrItemNum])
            futureAverages.append(np.mean(tempOutcomes))
            stDev.append(np.std(tempOutcomes))

        return futureAverages,stDev


# In[18]:

def sortBest(array):
    finalArr = []
    def getKey(val):
        return val['future'][-1]
    finalArr = sorted(array, key=getKey, reverse=True)
    return finalArr

bestCollect = []

def bestGo(val,curArr):
    global bestCollect
    try:
        #curArr = yahooLoad(val)
        curPat = currentPat(curArr)
        matchedPat,matchedEndInd = matchPats(patCollect,endingInd,curPat)
        futureAverages,stDev = plotting(matchedPat,matchedEndInd)
        totalDict = {'symbol': val,'matches': matchedPat,'current': curPat,'future': futureAverages, 'stDev': stDev, 'sharpe': futureAverages[-1]/stDev[-1]}
        bestCollect.append(totalDict)
    except:
        bestCollect.append({'error':'error'})
        pass


# In[19]:

arr = ['MMM','ABT','ABBV','ACN','ATVI','AYI','ADBE','AAP','AES','AET','AMG','AFL','A','GAS','APD','AKAM','ALK','AA','ALXN','ALLE','AGN','ADS','ALL','GOOGL','GOOG']#'MO','AMZN','AEE','AAL','AEP','AXP','AIG','AMT','AWK','AMP','ABC','AME','AMGN','APH','APC','ADI','ANTM','AON','APA','AIV','AAPL','AMAT','ADM','AJG','AIZ','T','ADSK','ADP','AN','AZO','AVGO','AVB','AVY','BHI','BLL','BAC','BCR','BAX','BBT','BDX','BBBY','BRK-B','BBY','BIIB','BLK','HRB','BA','BWA','BXP','BSX','BMY','BF-B','CHRW','CA','CVC','COG','CPB','COF','CAH','KMX','CCL','CAT','CBG','CBS','CELG','CNC','CNP','CTL','CERN','CF','SCHW','CHK','CVX','CMG','CB','CHD','CI','XEC','CINF','CTAS','CSCO','C','CFG','CTXS','CME','CMS','COH','CTSH','CL','CPGX','CMCSA','CMA','CAG','CXO','COP','ED','STZ','GLW','COST','CCI','CSRA','CSX','CMI','CVS','DHI','DHR','DRI','DVA','DE','DLPH','DAL','XRAY','DVN','DO','DLR','DFS','DISCA','DISCK','DG','DLTR','D','DOV','DOW','DPS','DTE','DD','DUK','DNB','ETFC','EMN','ETN','EBAY','ECL','EIX','EW','EA','EMC','EMR','ENDP','ETR','EOG','EQT','EFX','EQIX','EQR','ESS','EL','ES','EXC','EXPE','EXPD','ESRX','EXR','XOM','FFIV','FB','FAST','FRT','FDX','FIS','FITB','FSLR','FE','FISV','FLIR','FLS','FLR','FMC','FTI','FL','F','BEN','FCX','FTR','GPS','GRMN','GD','GE','GGP','GIS','GM','GPC','GILD','GPN','GS','GT','GWW','HAL','HBI','HOG','HAR','HRS','HIG','HAS','HCA','HCP','HP','HSIC','HES','HPE','HOLX','HD','HON','HRL','HST','HPQ','HUM','HBAN','ITW','ILMN','IR','INTC','ICE','IBM','IP','IPG','IFF','INTU','ISRG','IVZ','IRM','JBHT','JEC','JNJ','JCI','JPM','JNPR','KSU','K','KEY','KMB','KIM','KMI','KLAC','KSS','KHC','KR','LB','LLL','LH','LRCX','LM','LEG','LEN','LUK','LVLT','LLY','LNC','LLTC','LKQ','LMT','L','LOW','LYB','MTB','MAC','M','MNK','MRO','MPC','MAR','MMC','MLM','MAS','MA','MAT','MKC','MCD','MCK','MJN','MDT','MRK','MET','KORS','MCHP','MU','MSFT','MHK','TAP','MDLZ','MON','MNST','MCO','MS','MSI','MUR','MYL','NDAQ','NOV','NAVI','NTAP','NFLX','NWL','NFX','NEM','NWSA','NWS','NEE','NLSN','NKE','NI','NBL','JWN','NSC','NTRS','NOC','NRG','NUE','NVDA','ORLY','OXY','OMC','OKE','ORCL','OI','PCAR','PH','PDCO','PAYX','PYPL','PNR','PBCT','PEP','PKI','PRGO','PFE','PCG','PM','PSX','PNW','PXD','PBI','PNC','RL','PPG','PPL','PX','PCLN','PFG','PG','PGR','PLD','PRU','PEG','PSA','PHM','PVH','QRVO','QCOM','PWR','DGX','RRC','RTN','O','RHT','REGN','RF','RSG','RAI','RHI','ROK','COL','ROP','ROST','RCL','R','SPGI','CRM','SCG','SLB','SNI','STX','SEE','SRE','SHW','SIG','SPG','SWKS','SLG','SJM','SNA','SO','LUV','SWN','SE','STJ','SWK','SPLS','SBUX','HOT','STT','SRCL','SYK','STI','SYMC','SYF','SYY','TROW','TGT','TEL','TE','TGNA','TDC','TSO','TXN','TXT','BK','CLX','KO','HSY','MOS','TRV','DIS','TMO','TIF','TWX','TJX','TMK','TSS','TSCO','TDG','RIG','TRIP','FOXA','FOX','TYC','TSN','USB','UDR','ULTA','UA','UNP','UAL','UNH','UPS','URI','UTX','UHS','UNM','URBN','VFC','VLO','VAR','VTR','VRSN','VRSK','VZ','VRTX','VIAB','V','VNO','VMC','WMT','WBA','WM','WAT','WFC','HCN','WDC','WU','WRK','WY','WHR','WFM','WMB','WLTW','WEC','WYN','WYNN','XEL','XRX','XLNX','XL','XYL','YHOO','YUM','ZBH','ZION','ZTS']


pool = ThreadPool(4)
quoteCollect = pool.map(yahooLoad, arr)
pool.close()
pool.join()

bestCollect = []
for i in quoteCollect:
    for key,value in i.iteritems():
        bestGo(key,value)

finalBest = []
for val in bestCollect:
    if val['sharpe'] > 0.75:
        finalBest.append(val)

bestArr = sortBest(finalBest)

os.remove("best.pickle")
with open(r"best.pickle", "wb") as output_file:
    cPickle.dump(bestArr, output_file)
