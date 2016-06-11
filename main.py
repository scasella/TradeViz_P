from bottle import hook, route, run
from bottle import request, response
from bottle import post, get, put, delete

import os
from os import environ as env
from sys import argv

import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import urllib2
from multiprocessing.dummy import Pool as ThreadPool
import math

import json

_allow_origin = '*'
_allow_methods = 'GET'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'


priceArr = []
patCollect = []
endingInd = []
patLen = 24
futureE = 24
curPat = []
matchedPat = []
matchedEndInd = []
futureAverages = []
stDev = []
interval = 3600
gTicker = ""
theInd = 7
totalDict = {}

def percentChange(startPoint,currentPoint):
    try:
        x = ((float(currentPoint)-startPoint)/abs(startPoint))
        return x
    except:
        print(currentPoint, startPoint)
        return 0.00000000001

def loadQuote(val):
    global interval
    global priceArr
    global theInd
    global gTicker
    tempArr = []
    string = ""
    string = 'https://www.google.com/finance/getprices?q={0}&i={1}&p=200d&f=d,c,v'.format(val,interval)

    csv = urllib2.urlopen(string).readlines()
    for bar in xrange(8,len(csv)):
        offset,close,volume = csv[bar].split(',')
        if offset[0]!='a':
            tempArr.append(float(close))
    priceArr.append(tempArr)
    if val == gTicker:
        theInd = priceArr.index(tempArr)


def yahooLoad(val):
    global priceArr
    global theInd
    global gTicker
    tempArr = []
    string = ""
    string = 'http://ichart.finance.yahoo.com/table.csv?s={0}'.format(val)

    try:
        csv = urllib2.urlopen(string).readlines()
        #for bar in xrange(1,min(len(csv),500)):
        for bar in xrange(1,len(csv)):
            close = csv[bar].split(',')[6]
            close = float(close)
            tempArr.append(close)
        tempArr = tempArr[::-1]
        tempArr = np.array(tempArr, dtype=float)
        priceArr.append(tempArr)
        if val == gTicker:
            theInd = priceArr.index(tempArr)
            print(theInd)
    except:
        print()

def currentPat(tickerCol):
    global curPat
    global patLen
    curPat = []
    sliceLen = patLen
    curr = priceArr[tickerCol][-(sliceLen+1):]
    while curr[-2] == curr[-1]:
        sliceLen += 1
        curr = priceArr[tickerCol][-sliceLen:]
    i = 0
    while i < patLen:
        temp = percentChange(curr[i], curr[i + 1])
        curPat.append(temp)
        i += 1

def collectPats(tickerCol):
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


def sortPats(array):
    finalArr = []
    def getKey(tup):
        return tup[1]
    finalArr = sorted(array, key=getKey)
    return finalArr

def matchPats():
    colNum = 0
    global MSE
    global matchedEndInd
    global matchedPat
    global matchThresh
    global patCollect
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


def plotting(isPlotting):
    global futureAverages
    global futureE
    global stDev
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

        for arrItemNum in range(len(futurePercent[0])):
                tempOutcomes = []
                for arr in futurePercent:
                    tempOutcomes.append(arr[arrItemNum])
                futureAverages.append(np.mean(tempOutcomes))
                stDev.append(np.std(tempOutcomes))

def runGo(ticker,selection):
    global priceArr
    global patCollect
    global endingInd
    global matchedEndInd
    global curPat
    global matchedPat
    global futureAverages
    global stDev
    global patLen
    global totalDict
    global interval
    global theInd
    global gTicker

    gTicker = ticker

    if selection == 1:
        arr = [ticker,'GOOGL','AMZN','NFLX','MSFT','ORCL','MCD','KO',
                   'AGN','T','VZ','APA','XOM','M','MA','BAC','JPM','GS','NKE',
                   'JCP','HES','COP','JNJ','SBUX','F','GE','ABBV','WFC','SLB',
                   'GILD','MO','GE','V','WMT','PEP','QCOM']

        patLen = 10
        # Make the Pool of workers
        pool = ThreadPool(4)
        # Open the urls in their own threads
        # and return the results
        results = pool.map(yahooLoad, arr)
        #close the pool and wait for the work to finish
        pool.close()
        pool.join()
    elif selection == 2:
        arr = ['SPY','EURUSD','GOOGL','AMZN','USDJPY','NFLX','MSFT','ORCL','MCD','KO',
                   'AGN','T','VZ','APA','XOM','M','MA','BAC','JPM','GS','NKE','AUDJPY','GBPUSD',
                   'JCP','HES','COP','JNJ','SBUX','F','GE','ABBV']

        interval = 3600
        patLen = 24
        pool = ThreadPool(4)
        # Open the urls in their own threads
        # and return the results
        results = pool.map(loadQuote, arr)
        #close the pool and wait for the work to finish
        pool.close()
        pool.join()

    elif selection == 3:
        arr = ['SPY','EURUSD','GOOGL','AMZN','USDJPY','NFLX','MSFT','ORCL','MCD','KO',
                   'AGN','T','VZ','APA','XOM','M','MA','BAC','JPM','GS','NKE','AUDJPY','GBPUSD',
                   'JCP','HES','COP','JNJ','SBUX','F','GE','ABBV']

        interval = 900
        patLen = 24
        pool = ThreadPool(4)
        # Open the urls in their own threads
        # and return the results
        results = pool.map(loadQuote, arr)
        #close the pool and wait for the work to finish
        pool.close()
        pool.join()

    currentPat(theInd)
    collectPats(theInd)
    matchPats()
    plotting(False)
    totalDict = {'matches': matchedPat,'current': curPat,'future': futureAverages, 'stDev': stDev}
#except (RuntimeError, TypeError, NameError):
     #   totalDict = {'error':'error','error':'error','error':'error','error':'error'}
    priceArr = []
    patCollect = []
    endingInd = []
    matchedEndInd = []
    curPat = []
    matchedPat = []
    futureAverages = []
    stDev = []
    theInd = 7

@hook('after_request')
def enable_cors():
    '''Add headers to enable CORS'''

    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers

@get('/<tickerSubmit>/<numSelect>')
def main(tickerSubmit, numSelect):
    #try:
    #    try:
    runGo(str(tickerSubmit),int(numSelect))
    #    except:
    #        raise ValueError

    #except ValueError:
    #    response.status = 400
    #    return

    #except KeyError:
    #    response.status = 409
    #    return

    response.headers['Content-Type'] = 'application/json'
    #return 'hello world'
    return json.dumps(totalDict)

run(host='0.0.0.0', port=argv[1])
