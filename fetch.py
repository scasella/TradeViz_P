import urllib2
from multiprocessing.dummy import Pool as ThreadPool
import cPickle

exportArr = []

def yahooLoad(val):
    global exportArr
    string = ""
    tempArr = []
    string = 'http://ichart.finance.yahoo.com/table.csv?s={0}'.format(val)

    csv = urllib2.urlopen(string).readlines()
    #for bar in xrange(1,min(len(csv),500)):
    for bar in xrange(1,len(csv)):
        close = csv[bar].split(',')[6]
        close = float(close)
        tempArr.append(close)
    tempArr = tempArr[::-1]
    exportArr.append(tempArr)


def loadQuote(val,interval):
    global exportArr
    global interval
    tempArr = []
    string = ""
    string = 'https://www.google.com/finance/getprices?q={0}&i={1}&p=200d&f=d,c,v'.format(val,interval)

    csv = urllib2.urlopen(string).readlines()
    for bar in xrange(8,len(csv)):
        offset,close,volume = csv[bar].split(',')
        if offset[0]!='a':
            tempArr.append(float(close))
    exportArr.append(tempArr)



arr = ['A','AA','AAL','AAP','AAPL','ABBV','ABC','ABT','ACN','ADBE','ADI','ADM','ADP','ADS','ADSK','AEE',
'AEP','AES','AET','AFL','AGN','AIG','AIV','AIZ','AKAM','ALK','ALL','ALLE','ALXN','AMAT','AME','AMG','AMGN','AMP',
'AMT','AMZN','AN','ANTM','AON','APA','APC','APD','APH','ATVI','AVB','AVGO','AVY','AWK','AXP','AYI','AZO','BA','BAC',
'BAX','BBBY','BBT','BBY','BCR','BEN']

exportArr = []

pool = ThreadPool(4)
pool.map(yahooLoad, arr)

with open(r"one.pickle", "wb") as output_file:
    cPickle.dump("", output_file)
with open(r"one.pickle", "wb") as output_file:
    cPickle.dump(exportArr, output_file)



arr = ['A','AA','AAL','AAP','AAPL','ABBV','ABC','ABT','ACN','ADBE','ADI','ADM','ADP','ADS','ADSK','AEE',
'AEP','AES','AET','AFL','AGN','AIG','AIV','AIZ','AKAM','ALK','ALL','ALLE','ALXN','AMAT','AME','AMG','AMGN','AMP',
'AMT','AMZN','AN','ANTM','AON','APA','APC','APD','APH','ATVI','AVB','AVGO','AVY','AWK','AXP','AYI','AZO','BA','BAC',
'BAX','BBBY','BBT','BBY','BCR','BEN']

exportArr = []

interval = 3600 
pool = ThreadPool(4)
pool.map(loadQuote, arr)

with open(r"two.pickle", "wb") as output_file:
    cPickle.dump("", output_file)
with open(r"two.pickle", "wb") as output_file:
    cPickle.dump(exportArr, output_file)



arr = ['A','AA','AAL','AAP','AAPL','ABBV','ABC','ABT','ACN','ADBE','ADI','ADM','ADP','ADS','ADSK','AEE',
'AEP','AES','AET','AFL','AGN','AIG','AIV','AIZ','AKAM','ALK','ALL','ALLE','ALXN','AMAT','AME','AMG','AMGN','AMP',
'AMT','AMZN','AN','ANTM','AON','APA','APC','APD','APH','ATVI','AVB','AVGO','AVY','AWK','AXP','AYI','AZO','BA','BAC',
'BAX','BBBY','BBT','BBY','BCR','BEN']

exportArr = []

interval = 900 
pool = ThreadPool(4)
pool.map(loadQuote, arr)

with open(r"three.pickle", "wb") as output_file:
    cPickle.dump("", output_file)
with open(r"three.pickle", "wb") as output_file:
    cPickle.dump(exportArr, output_file)

