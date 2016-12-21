# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 23:55:42 2016

@author: TroyRuan
"""
# 2016 US Preliminary 'Super Tuesday': 2016.03.01
## UK Stock Data Set-ups:
import pandas as pd # load "numpy"
import numpy as np

# Read in UK Data:
uk = pd.read_csv('lseg.csv') 
uk = pd.DataFrame({'Date':uk.Date,
                   'Close':uk.Close,
                   'Stock':uk.Stockname,
                   'Volume':uk.Volume})
ukstock = list(set(uk.Stock))
ukstock = pd.DataFrame({'Stock':ukstock})

# Read in currency exchange rate:
cur = pd.read_csv('Currency_Rate.csv')
for i in range(len(cur)):
    if cur.Rate[i] == ('ND'):
        cur.Rate[i] = cur.Rate[i-1]

import datetime
cur['Date']=pd.to_datetime(cur['Date']) # Convert type from object to float
cur['Rate']=cur['Rate'].convert_objects(convert_numeric=True)

# Select data withtin certain time frame and apply daily exchange rate:
import datetime
uk['Date']=pd.to_datetime(uk['Date']) # Convert type from object to float

priordate = uk['Date'][(uk.Date > '2016-02-01') & (uk.Date <= '2016-03-01')]
priorstock = uk['Stock'][(uk.Date > '2016-02-01') & (uk.Date <= '2016-03-01')]
priorclose = uk['Close'][(uk.Date > '2016-02-01') & (uk.Date <= '2016-03-01')]
prior = pd.DataFrame({'Date':priordate,
                      'Stock':priorstock,
                      'Close':priorclose})

priormean = []
for i in range(len(ukstock)):
    stkmean = prior.Close[prior.Stock == ukstock.Stock[i]].mean()
    priormean.append(stkmean)

postdate = uk['Date'][(uk.Date > '2016-03-01') & (uk.Date <= '2016-04-01')]
poststock = uk['Stock'][(uk.Date > '2016-03-01') & (uk.Date <= '2016-04-01')]
postclose = uk['Close'][(uk.Date > '2016-03-01') & (uk.Date <= '2016-04-01')]
post = pd.DataFrame({'Date':postdate,
                      'Stock':poststock,
                      'Close':postclose})

postmean = []
for i in range(len(ukstock)):
    stkmean = post.Close[post.Stock == ukstock.Stock[i]].mean()
    postmean.append(stkmean)


# Apply inflation rate:
CPI = pd.read_csv('UK_Monthly_CPI.csv') 
febcpi = float(CPI.cpi[CPI.Month == '2016 FEB'])
marcpi = float(CPI.cpi[CPI.Month == '2016 MAR'])
inf = (marcpi - febcpi)/febcpi


realpriormean = []
for i in range(len(priormean)):
    realprior = priormean[i]*(1+inf)
    realpriormean.append(realprior)
priorstd = np.std(priormean)
priorn = len(priormean)
realpostmean = postmean
poststd = np.std(postmean)
postn = len(postmean)


# Statistics Analysis:
stockdiff = []
for i in range(len(realpostmean)):
    diff = realpostmean[i]-realpriormean[i]
    stockdiff.append(diff)

# Creat line plot to initiate hypothesis:
plotx = range(len(stockdiff))
plotdata = pd.DataFrame({'Stock':plotx,
                         'Diff':stockdiff})
plotdata.plot.scatter(x='Stock',y='Diff',title='2016 "Super Tuesday" (2016.03.01) Effect on UK Market') 

# Confidence interval:
diffmean = np.mean(stockdiff)
diffstd = np.std(stockdiff,ddof=1)
from scipy import stats
t=stats.t.ppf(1-0.05/2,len(stockdiff))    # compute critical t value
UB = diffmean + t*diffstd
LB = diffmean - t*diffstd
CI = [LB, UB]

# Two-sample t-test:
from scipy.stats import norm
tval = diffmean/diffstd
pval = (1 - stats.t.cdf(abs(tval),len(stockdiff)-1))*2
if pval < 0.05:
    print('There is difference in stock prices before and after the event')
else:
    print('There is NO difference in stock prices before and after the event')


# Look at trading activities by volume:
vol = []
alldate = np.unique(uk.Date[(uk.Date > '2008-10-04') & (uk.Date <= '2008-12-04')])
alldate = pd.to_datetime(alldate)
# Get total volume of these stocks every day within the period:
for i in range(len(alldate)):
    volume = uk.Volume[uk.Date == alldate[i]].sum()
    vol.append(volume)
    i = i + 1

voldate = []
for i in range(len(alldate)):
    date = str(alldate[i].month) + str('/') + str(alldate[i].day)
    voldate.append(date)

volumedata = pd.DataFrame({'Date':voldate,
                           'TotalVolume':vol})
volumedata.plot.bar(x='Date', y = 'TotalVolume',title='2016 "Super Tuesday" (2016.03.01) Effect on UK Market')

