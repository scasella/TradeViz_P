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
import cPickle
#from best import bestArr

import json

_allow_origin = '*'
_allow_methods = 'GET'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'


patLen = 24
futureE = 24
totalDict = {}

def percentChange(startPoint,currentPoint):
    try:
        x = ((float(currentPoint)-startPoint)/abs(startPoint))
        return x
    except:
        print(currentPoint, startPoint)
        return 0.00000000001

def loadQuote(val, interval):
    priceArr = []
    curArr = []
    tempArr = []
    string = ""
    string = 'https://www.google.com/finance/getprices?q={0}&i={1}&p=200d&f=d,c'.format(val,interval)

    csv = urllib2.urlopen(string).readlines()
    for bar in xrange((len(csv)-patLen-100),len(csv)):
        offset,close = csv[bar].split(',')
        if offset[0]!='a':
            tempArr.append(float(close))
    curArr.append(tempArr)
    if interval == 3600:
        with open(r"two.pickle", "rb") as input_file:
            e = cPickle.load(input_file)
            priceArr = e
    elif interval == 900:
        with open(r"three.pickle", "rb") as input_file:
            e = cPickle.load(input_file)
            priceArr = e
    return priceArr, curArr


def yahooLoad(val):
    priceArr = []
    curArr = []
    tempArr = []
    string = ""
    string = 'http://ichart.finance.yahoo.com/table.csv?s={0}'.format(val)

    csv = urllib2.urlopen(string).readlines()
    #for bar in xrange(1,min(len(csv),500)):
    for bar in xrange(1,min(100,len(csv))):
        close = csv[bar].split(',')[6]
        tempArr.append(float(close))
    tempArr = tempArr[::-1]
    curArr.append(tempArr)
    with open(r"one.pickle", "rb") as input_file:
        e = cPickle.load(input_file)
        priceArr = e
    return priceArr, curArr


def currentPat(curArr):
    curPat = []
    sliceLen = patLen
    curr = curArr[0][-(sliceLen+1):]
    #while curr[-2] == curr[-1]:
    #    sliceLen += 1
    #    curr = curArr[0][-(sliceLen+1):]
    i = 0
    while i < patLen:
        temp = percentChange(curr[i], curr[i + 1])
        curPat.append(temp)
        i += 1
    return curPat


def collectPats(priceArr):
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
            sIndex += (patLen/2)
        patCollect.append(tempCollect)
        endingInd.append(tempEnd)
    return patCollect, endingInd


def sortPats(array):
    finalArr = []
    def getKey(tup):
        return tup[1]
    finalArr = sorted(array, key=getKey)
    return finalArr


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


def plotting(matchedPat,matchedEndInd,priceArr):
    futureLine = []
    futurePercent = []
    futureAverages = []
    stDev = []
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
    return futureAverages,stDev

def runGo(ticker,selection):
    global totalDict
    global patLen

    priceArr = []
    curArr = []

    if selection == 1:

        patLen = 10
        priceArr,curArr = yahooLoad(ticker)

    elif selection == 2:

        patLen = 24
        priceArr,curArr = loadQuote(ticker,3600)

    elif selection == 3:

        patLen = 24
        priceArr,curArr = loadQuote(ticker,900)

    curPat = currentPat(curArr)
    patCollect,endingInd = collectPats(priceArr)
    matchedPat,matchedEndInd = matchPats(patCollect,endingInd,curPat)
    futureAverages,stDev = plotting(matchedPat,matchedEndInd,priceArr)
    totalDict = {'matches': matchedPat,'current': curPat,'future': futureAverages, 'stDev': stDev}


@hook('after_request')
def enable_cors():
    '''Add headers to enable CORS'''

    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers

@get('/<tickerSubmit>/<numSelect:int>')
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

@get('/best')
def best():

    t = []

    with open(r"best.pickle", "rb") as input_file:
        t = cPickle.load(input_file)

    response.headers['Content-Type'] = 'application/json'
    return json.dumps(t)

@get('/quotes')
def quotes():
    arr = ['SPX','.DJI','.IXIC','TLT','AAPL','GOOGL','AMZN','NFLX','BAC','JPM','MCD','TSLA','MCD','NKE','MSFT',
      'XLE','XLF','QQQ','FB','VZ','GE','BA','HD','DIS','JNJ','GS','PCLN','MS','TJX','M','SBUX','XOM','V','MA',
      'XLU','IBM','INTC','XLV','XLI','IYR','XLY','EEM','FXI','GLD','SLV','GDX','FXE','UUP','HYG','SMH']

    string = ""
    for ind,val in enumerate(arr):
        if ind != (len(arr)-1):
            string = string+val+","
        else:
            string = string+val

    u = urllib2.urlopen('http://finance.google.com/finance/info?client=ig&q='+string)
    content = u.read()
    dat = json.loads(content[3:])

    response.headers['Content-Type'] = 'application/json'
    return json.dumps(dat)

@get('/quotes/<sym>')
def quoteSym(sym):

    u = urllib2.urlopen('http://finance.google.com/finance/info?client=ig&q='+str(sym))
    content = u.read()
    dat = json.loads(content[3:])

    response.headers['Content-Type'] = 'application/json'
    return json.dumps(dat)

run(host='0.0.0.0', port=argv[1])
