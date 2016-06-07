from bottle import hook, route, run
from bottle import request, response
from bottle import post, get, put, delete

import os
from os import environ as env
from sys import argv

import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import urllib
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
extraArr = []
futureFinal = []
toExtra = []

curCollect = []
matchedCollect = []
futureCollect = []
extraCollect = []


def percentChange(startPoint,currentPoint):
    for i in range(1000):
        try:
            x = ((float(currentPoint)-startPoint)/abs(startPoint))
            return x
        except:
            print(currentPoint, startPoint)
            return 0.00000000001

def loadQuote(tickerArr,interval):
    global priceArr
    priceArr = []
    for i in tickerArr:
        tempArr = []
        string = 'https://www.google.com/finance/getprices?q={0}&i={1}&p=200d&f=d,c,v'.format(i,interval)
        csv = urllib.urlopen(string).readlines()
        for bar in xrange(8,len(csv)):
            if csv[bar].count(',')!=2: continue
            offset,close,volume = csv[bar].split(',')
            if offset[0]=='a':
                day = float(offset[1:])
                offset = 0
            else:
                offset = float(offset)
                offset,close,volume = [float(x) for x in [offset,close,volume]]
                tempArr.append(close)
        tempArr = np.array(tempArr, dtype=float)
        priceArr.append(tempArr[:-100])

def yahooLoad(tickerArr):
    global priceArr
    priceArr = []
    for val in tickerArr:
        tempArr = []
        string = ""
        if len(val) < 6:
            string = 'http://ichart.finance.yahoo.com/table.csv?s={0}'.format(val)

            csv = urllib.urlopen(string).readlines()
            for bar in xrange(1,len(csv)):
                close = csv[bar].split(',')[6]
                close = float(close)
                tempArr.append(close)
        tempArr = tempArr[::-1]
        tempArr = np.array(tempArr, dtype=float)
        priceArr.append(tempArr)

def currentPat(tickerCol):
    global curPat
    global patLen
    curPat = []
    sliceLen = patLen+1
    curr = priceArr[tickerCol][-sliceLen:]
    while curr[2] == curr[4]:
        sliceLen += patLen
        curr = priceArr[tickerCol][-sliceLen:]
    i = 0
    while i < patLen:
        temp = percentChange(curr[i], curr[i + 1])
        curPat.append(temp)
        i += 1

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

            if percentChange(each[sIndex+patLen*0.75],each[sIndex+patLen]) > 0.0001 and percentChange(each[sIndex+patLen*0.25],each[sIndex+patLen]) > 0.0001 and percentChange(each[sIndex+patLen*0.50],each[sIndex+patLen]) > 0.0001:
                while inc <= patLen:
                    temp = percentChange(each[sIndex + inc -1], each[sIndex + inc])
                    inc += 1
                    tempPat.append(temp)
                tempCollect.append(tempPat)
                tempEnd.append(sIndex+patLen)
            sIndex += (patLen/2)
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
            weighting = []
            incr = 0
            for i in mseCollect:
                if incr > len(mseCollect)/2:
                    weighting.append(math.sqrt(i))
                else:
                    weighting.append(i)
                incr += 1
            #mseAvg = np.average(weighting)
            mseAvg = np.average(mseCollect)
            bestMatches.append(([row,colInd,endingInd[colInd][rowInd]],mseAvg))
    test = sortPats(bestMatches)
    for item in test[:10]:
        matchedPat.append(item[0][0])
        matchedEndInd.append((item[0][1],item[0][2]))

def plotting(toOutput):
    global curPat
    global futureFinal
    futureFinal = []
    global matchedPat
    global futureE
    global toExtra
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
                toExtra.append([futureAverages[-1],np.std(tempOutcomes)])


def runGo(ticker,selection):
    global curPat
    global matchedPat
    global finalFuture
    global toExtra
    global patLen
    if selection == 1:
        yahooLoad([ticker,'GOOGL','AMZN','NFLX','MSFT','ORCL','MCD','KO',
                   'AGN','T','VZ','APA','XOM'])#'M','MA','BAC','JPM','GS','NKE',
                   #'JCP','HES','COP','JNJ','SBUX','F','GE','ABBV'])
        patLen = 10
    elif selection == 2:
        loadQuote([ticker,'EURUSD','GOOGL','AMZN','USDJPY','NFLX','MSFT','ORCL','MCD','KO',
                   'AGN','T','VZ','APA','XOM','M','MA','BAC','JPM','GS','NKE','AUDJPY','GBPUSD',
                   'JCP','HES','COP','JNJ','SBUX','F','GE','ABBV'],3600)
        patLen = 24
    elif selection == 3:
        loadQuote([ticker,'EURUSD','GOOGL','AMZN','USDJPY','NFLX','MSFT','ORCL','MCD','KO',
                   'AGN','T','VZ','APA','XOM','M','MA','BAC','JPM','GS','NKE','AUDJPY','GBPUSD',
                   'JCP','HES','COP','JNJ','SBUX','F','GE','ABBV'],900)
        patLen = 24
    try:
        currentPat(0)
        collectPats()
        matchPats()
        plotting(True)

        curCollect.append(curPat)
        matchedCollect.append(matchedPat)
        futureCollect.append(futureFinal)
        extraCollect.append(toExtra)
    except (RuntimeError, TypeError, NameError):
        matchedCollect.append(['error'])
        futureCollect.append(['error'])
        extraCollect.append(['error'])
        curCollect.append(['error'])





@hook('after_request')
def enable_cors():
    '''Add headers to enable CORS'''

    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers

@get('/<tickerSubmit>')
def main(tickerSubmit):
    try:
        try:
            runGo(tickerSubmit,1)
            runGo(tickerSubmit,2)
            runGo(tickerSubmit,3)
        except:
            raise ValueError

        if data is None:
            raise ValueError

    except ValueError:
        response.status = 400
        return

    except KeyError:
        response.status = 409
        return

    response.headers['Content-Type'] = 'application/json'
    #return 'hello world'
    return json.dumps({'matches': matchedCollect,'current': curCollect,'future': futureCollect, 'extra': extraCollect})

run(host='0.0.0.0', port=argv[1])
