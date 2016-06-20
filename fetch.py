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


def loadQuote(val):
    global exportArr
    global interval
    tempArr = []
    string = ""
    string = 'https://www.google.com/finance/getprices?q={0}&i={1}&p=200d&f=d,c'.format(val,interval)

    csv = urllib2.urlopen(string).readlines()
    for bar in xrange(7,len(csv)):
        offset,close = csv[bar].split(',')
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
    cPickle.dump(exportArr, output_file)



arr = ['MMM','ABT','ABBV','ACN','ATVI','AYI','ADBE','AAP','AES','AET','AMG','AFL','A','GAS','APD','AKAM',
'ALK','AA','ALXN','ALLE','AGN','ADS','ALL','GOOGL','GOOG','MO','AMZN','AEE','AAL','AEP','AXP','AIG','AMT',
'AWK','AMP','ABC','AME','AMGN','APH','APC','ADI','ANTM','AON','APA','AIV','AAPL','AMAT','ADM','AJG','AIZ','T','ADSK','ADP',
'AN','AZO','AVGO','AVB','AVY','BHI','BLL','BAC','BCR','BAX','BBT','BDX','BBBY','BRK-B','BBY','BIIB','BLK','HRB','BA','BWA','BXP',
'BSX','BMY','BF-B','CHRW','CA','CVC','COG','CPB','COF','CAH','KMX','CCL','CAT','CBG','CBS','CELG','CNC','CNP','CTL','CERN','CF',
'SCHW','CHK','CVX','CMG','CB','CHD','CI','XEC','CINF','CTAS','CSCO','C','CFG','CTXS','CME','CMS','COH','CTSH','CL','CPGX','CMCSA',
'CMA','CAG','CXO','COP','ED','STZ','GLW','COST','CCI','CSRA','CSX','CMI','CVS','DHI','DHR','DRI','DVA','DE','DLPH','DAL','XRAY',
'DVN','DO','DLR','DFS','DISCA','DISCK','DG','DLTR','D','DOV','DOW','DPS','DTE','DD','DUK','DNB','ETFC','EMN','ETN','EBAY','ECL',
'EIX','EW','EA','EMC','EMR','ENDP','ETR','EOG','EQT','EFX','EQIX','EQR','ESS','EL','ES','EXC','EXPE','EXPD','ESRX','EXR','XOM',
'FFIV','FB','FAST','FRT','FDX','FIS','FITB','FSLR','FE','FISV','FLIR','FLS','FLR','FMC','FTI','FL','F','BEN','FCX','FTR','GPS',
'GRMN','GD','GE','GGP','GIS','GM','GPC','GILD','GPN','GS','GT','GWW','HAL','HBI','HOG','HAR','HRS','HIG','HAS','HCA','HCP','HP',
'HSIC','HES','HPE','HOLX','HD','HON','HRL','HST','HPQ','HUM','HBAN','ITW','ILMN','IR','INTC','ICE','IBM','IP','IPG','IFF','INTU',
'ISRG','IVZ','IRM','JBHT','JEC','JNJ','JCI','JPM','JNPR','KSU','K','KEY','KMB','KIM','KMI','KLAC','KSS','KHC','KR','LB','LLL','LH',
'LRCX','LM','LEG','LEN','LUK','LVLT','LLY','LNC','LLTC','LKQ','LMT','L','LOW','LYB','MTB','MAC','M','MNK','MRO','MPC','MAR','MMC',
'MLM','MAS','MA','MAT','MKC','MCD','MCK','MJN','MDT','MRK','MET','KORS','MCHP','MU','MSFT','MHK','TAP','MDLZ','MON','MNST','MCO','MS',
'MSI','MUR','MYL','NDAQ','NOV','NAVI','NTAP','NFLX','NWL','NFX','NEM','NWSA','NWS','NEE','NLSN','NKE','NI','NBL','JWN','NSC','NTRS',
'NOC','NRG','NUE','NVDA','ORLY','OXY','OMC','OKE','ORCL','OI','PCAR','PH','PDCO','PAYX','PYPL','PNR','PBCT','PEP','PKI','PRGO','PFE',
'PCG','PM','PSX','PNW','PXD','PBI','PNC','RL','PPG','PPL','PX','PCLN','PFG','PG','PGR','PLD','PRU','PEG','PSA','PHM','PVH','QRVO',
'QCOM','PWR','DGX','RRC','RTN','O','RHT','REGN','RF','RSG','RAI','RHI','ROK','COL','ROP','ROST','RCL','R','SPGI','CRM','SCG','SLB',
'SNI','STX','SEE','SRE','SHW','SIG','SPG','SWKS','SLG','SJM','SNA','SO','LUV','SWN','SE','STJ','SWK','SPLS','SBUX','HOT','STT','SRCL',
'SYK','STI','SYMC','SYF','SYY','TROW','TGT','TEL','TE','TGNA','TDC','TSO','TXN','TXT','BK','CLX','KO','HSY','MOS','TRV','DIS','TMO',
'TIF','TWX','TJX','TMK','TSS','TSCO','TDG','RIG','TRIP','FOXA','FOX','TYC','TSN','USB','UDR','ULTA','UA','UNP','UAL','UNH','UPS',
'URI','UTX','UHS','UNM','URBN','VFC','VLO','VAR','VTR','VRSN','VRSK','VZ','VRTX','VIAB','V','VNO','VMC','WMT','WBA','WM','WAT','WFC',
'HCN','WDC','WU','WRK','WY','WHR','WFM','WMB','WLTW','WEC','WYN','WYNN','XEL','XRX','XLNX','XL','XYL','YHOO','YUM','ZBH','ZION','ZTS']

exportArr = []

interval = 3600 
pool = ThreadPool(4)
pool.map(loadQuote, arr)

with open(r"two.pickle", "wb") as output_file:
    cPickle.dump(exportArr, output_file)



arr = ['MMM','ABT','ABBV','ACN','ATVI','AYI','ADBE','AAP','AES','AET','AMG','AFL','A','GAS','APD','AKAM',
'ALK','AA','ALXN','ALLE','AGN','ADS','ALL','GOOGL','GOOG','MO','AMZN','AEE','AAL','AEP','AXP','AIG','AMT',
'AWK','AMP','ABC','AME','AMGN','APH','APC','ADI','ANTM','AON','APA','AIV','AAPL','AMAT','ADM','AJG','AIZ','T','ADSK','ADP',
'AN','AZO','AVGO','AVB','AVY','BHI','BLL','BAC','BCR','BAX','BBT','BDX','BBBY','BRK-B','BBY','BIIB','BLK','HRB','BA','BWA','BXP',
'BSX','BMY','BF-B','CHRW','CA','CVC','COG','CPB','COF','CAH','KMX','CCL','CAT','CBG','CBS','CELG','CNC','CNP','CTL','CERN','CF',
'SCHW','CHK','CVX','CMG','CB','CHD','CI','XEC','CINF','CTAS','CSCO','C','CFG','CTXS','CME','CMS','COH','CTSH','CL','CPGX','CMCSA',
'CMA','CAG','CXO','COP','ED','STZ','GLW','COST','CCI','CSRA','CSX','CMI','CVS','DHI','DHR','DRI','DVA','DE','DLPH','DAL','XRAY',
'DVN','DO','DLR','DFS','DISCA','DISCK','DG','DLTR','D','DOV','DOW','DPS','DTE','DD','DUK','DNB','ETFC','EMN','ETN','EBAY','ECL',
'EIX','EW','EA','EMC','EMR','ENDP','ETR','EOG','EQT','EFX','EQIX','EQR','ESS','EL','ES','EXC','EXPE','EXPD','ESRX','EXR','XOM',
'FFIV','FB','FAST','FRT','FDX','FIS','FITB','FSLR','FE','FISV','FLIR','FLS','FLR','FMC','FTI','FL','F','BEN','FCX','FTR','GPS',
'GRMN','GD','GE','GGP','GIS','GM','GPC','GILD','GPN','GS','GT','GWW','HAL','HBI','HOG','HAR','HRS','HIG','HAS','HCA','HCP','HP',
'HSIC','HES','HPE','HOLX','HD','HON','HRL','HST','HPQ','HUM','HBAN','ITW','ILMN','IR','INTC','ICE','IBM','IP','IPG','IFF','INTU',
'ISRG','IVZ','IRM','JBHT','JEC','JNJ','JCI','JPM','JNPR','KSU','K','KEY','KMB','KIM','KMI','KLAC','KSS','KHC','KR','LB','LLL','LH',
'LRCX','LM','LEG','LEN','LUK','LVLT','LLY','LNC','LLTC','LKQ','LMT','L','LOW','LYB','MTB','MAC','M','MNK','MRO','MPC','MAR','MMC',
'MLM','MAS','MA','MAT','MKC','MCD','MCK','MJN','MDT','MRK','MET','KORS','MCHP','MU','MSFT','MHK','TAP','MDLZ','MON','MNST','MCO','MS',
'MSI','MUR','MYL','NDAQ','NOV','NAVI','NTAP','NFLX','NWL','NFX','NEM','NWSA','NWS','NEE','NLSN','NKE','NI','NBL','JWN','NSC','NTRS',
'NOC','NRG','NUE','NVDA','ORLY','OXY','OMC','OKE','ORCL','OI','PCAR','PH','PDCO','PAYX','PYPL','PNR','PBCT','PEP','PKI','PRGO','PFE',
'PCG','PM','PSX','PNW','PXD','PBI','PNC','RL','PPG','PPL','PX','PCLN','PFG','PG','PGR','PLD','PRU','PEG','PSA','PHM','PVH','QRVO',
'QCOM','PWR','DGX','RRC','RTN','O','RHT','REGN','RF','RSG','RAI','RHI','ROK','COL','ROP','ROST','RCL','R','SPGI','CRM','SCG','SLB',
'SNI','STX','SEE','SRE','SHW','SIG','SPG','SWKS','SLG','SJM','SNA','SO','LUV','SWN','SE','STJ','SWK','SPLS','SBUX','HOT','STT','SRCL',
'SYK','STI','SYMC','SYF','SYY','TROW','TGT','TEL','TE','TGNA','TDC','TSO','TXN','TXT','BK','CLX','KO','HSY','MOS','TRV','DIS','TMO',
'TIF','TWX','TJX','TMK','TSS','TSCO','TDG','RIG','TRIP','FOXA','FOX','TYC','TSN','USB','UDR','ULTA','UA','UNP','UAL','UNH','UPS',
'URI','UTX','UHS','UNM','URBN','VFC','VLO','VAR','VTR','VRSN','VRSK','VZ','VRTX','VIAB','V','VNO','VMC','WMT','WBA','WM','WAT','WFC',
'HCN','WDC','WU','WRK','WY','WHR','WFM','WMB','WLTW','WEC','WYN','WYNN','XEL','XRX','XLNX','XL','XYL','YHOO','YUM','ZBH','ZION','ZTS']

exportArr = []

interval = 900 
pool = ThreadPool(4)
pool.map(loadQuote, arr)

with open(r"three.pickle", "wb") as output_file:
    cPickle.dump(exportArr, output_file)

