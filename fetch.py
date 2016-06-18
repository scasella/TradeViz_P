import urllib2
from multiprocessing.dummy import Pool as ThreadPool
import cPickle

exportArr = []
interval = 0

def yahooLoad(val):
    global exportArr
    exportArr = []
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


def loadQuote(val):
    global exportArr
    global interval
    exportArr = []
    tempArr = []
    string = ""
    string = 'https://www.google.com/finance/getprices?q={0}&i={1}&p=200d&f=d,c,v'.format(val,interval)

    csv = urllib2.urlopen(string).readlines()
    for bar in xrange(8,min(100,len(csv))):
        offset,close,volume = csv[bar].split(',')
        if offset[0]!='a':
            tempArr.append(float(close))
    exportArr.append(tempArr)



arr = ['GOOGL','AMZN','NFLX','MSFT','ORCL','MCD','KO',
       'AGN','T','VZ','APA','XOM','M','MA','BAC','JPM','GS','NKE',
       'JCP','HES','COP','JNJ','SBUX','F','GE','ABBV','WFC','SLB',
       'GILD','MO','GE','V','WMT','PEP','QCOM']

pool = ThreadPool(4)
pool.map(yahooLoad, arr)
pool.close()
pool.join()

with open(r"one.pickle", "wb") as output_file:
    cPickle.dump("", output_file)
with open(r"one.pickle", "wb") as output_file:
    cPickle.dump(exportArr, output_file)



arr = ['GOOGL','AMZN','NFLX','MSFT','ORCL','MCD','KO',
       'AGN','T','VZ','APA','XOM','M','MA','BAC','JPM','GS','NKE',
       'JCP','HES','COP','JNJ','SBUX','F','GE','ABBV','WFC','SLB',
       'GILD','MO','GE','V','WMT','PEP','QCOM']

interval = 3600
pool = ThreadPool(4)
pool.map(loadQuote, arr)
pool.close()
pool.join()

with open(r"two.pickle", "wb") as output_file:
    cPickle.dump("", output_file)
with open(r"two.pickle", "wb") as output_file:
    cPickle.dump(exportArr, output_file)



arr = ['GOOGL','AMZN','NFLX','MSFT','ORCL','MCD','KO',
       'AGN','T','VZ','APA','XOM','M','MA','BAC','JPM','GS','NKE',
       'JCP','HES','COP','JNJ','SBUX','F','GE','ABBV','WFC','SLB',
       'GILD','MO','GE','V','WMT','PEP','QCOM']

interval = 900
pool = ThreadPool(4)
pool.map(loadQuote, arr)
pool.close()
pool.join()

with open(r"three.pickle", "wb") as output_file:
    cPickle.dump("", output_file)
with open(r"three.pickle", "wb") as output_file:
    cPickle.dump(exportArr, output_file)
