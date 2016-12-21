# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 23:26:45 2016

@author: TroyRuan
"""
## Greek Crisis - First Eurozone country to receive bailout: 2010.05.02
## US Stock Data Set-ups:
import pandas as pd # load "numpy"
import numpy as np

# Read in US Data:
us = pd.read_csv('nasdaq.csv') 
us = pd.DataFrame({'Date':us.date,
                   'Close':us.close,
                   'Stock':us.Stockname,
                   'Volume':us.volume})
usstock = list(set(us.Stock))
usstock = pd.DataFrame({'Stock':usstock})

# Select data withtin certain time frame:
# 2010.04.02-2010.06.02:

import datetime
us['Date']=pd.to_datetime(us['Date']) # Convert type from object to float

priordate = us['Date'][(us.Date > '2010-04-02') & (us.Date <= '2010-05-02')]
priorstock = us['Stock'][(us.Date > '2010-04-02') & (us.Date <= '2010-05-02')]
priorclose = us['Close'][(us.Date > '2010-04-02') & (us.Date <= '2010-05-02')]
prior = pd.DataFrame({'Date':priordate,
                      'Stock':priorstock,
                      'Close':priorclose})

priormean = []
for i in range(len(usstock)):
    stkmean = prior.Close[prior.Stock == usstock.Stock[i]].mean()
    priormean.append(stkmean)

postdate = us['Date'][(us.Date > '2010-05-02') & (us.Date <= '2010-06-02')]
poststock = us['Stock'][(us.Date > '2010-05-02') & (us.Date <= '2010-06-02')]
postclose = us['Close'][(us.Date > '2010-05-02') & (us.Date <= '2010-06-02')]
post = pd.DataFrame({'Date':postdate,
                      'Stock':poststock,
                      'Close':postclose})

postmean = []
for i in range(len(usstock)):
    stkmean = post.Close[post.Stock == usstock.Stock[i]].mean()
    postmean.append(stkmean)


# Calculate inflation rate:
CPI = pd.read_csv('US_Monthly_CPI.csv') 
aprcpi = float(CPI.VALUE[CPI.MONTH == '2010/4/1'])
maycpi = float(CPI.VALUE[CPI.MONTH == '2010/5/1'])
inf = (maycpi - aprcpi)/aprcpi

# Apply inflation rate to prices:
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

# Creat scatter plot to initiate hypothesis:
plotx = range(30)
plotdata = pd.DataFrame({'Stock':plotx,
                         'Diff':stockdiff})
plotdata.plot.scatter(x='Stock',y='Diff',c='r',title='Greek Bailout (2010.05.02) Effect on US Market') 

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
alldate = np.unique(us.Date[(us.Date > '2008-10-04') & (us.Date <= '2008-12-04')])
alldate = pd.to_datetime(alldate)
# Get total volume of these stocks every day within the period:
for i in range(len(alldate)):
    volume = (us.Volume[us.Date == alldate[i]])
    volsum = 0    
    for j in range(len(stockdiff)):
        newvol = int(volume.iloc[j]) 
        volsum = volsum + newvol
        j = j + 1
    vol.append(volsum) 
    i = i + 1

voldate = []
for i in range(len(alldate)):
    date = str(alldate[i].month) + str('/') + str(alldate[i].day)
    voldate.append(date)

volumedata = pd.DataFrame({'Date':voldate,
                           'TotalVolume':vol})
volumedata.plot.bar(x='Date', y = 'TotalVolume',color='r',title='Greek Bailout (2010.05.02) Effect on US Market')
