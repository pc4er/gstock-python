### Note:
# This file was used to organize historical London Stock Exchange data from vaious stocks
# and convert them into a csv file
# Because of the large number of raw data files, raw data are not included in 
# the zip package


import pandas as pd # load "numpy"
import numpy as np

#NASDAQ data
import glob # 'glob' searches for files
# '*.csv' selects files ending in '.csv'


filelist = glob.glob('*.csv') 
# Can concatenate the dataframes into one large dataframe
# Concatenate df1 and df2 by rows
dflseg = pd.DataFrame()
for b in filelist:
    newdf = pd.read_csv(b)
    str = b
    i= str.find(".")
    stockname=str[0:i]
    newdf['Stockname']=[stockname]*len(newdf) #add the stock names
    dflseg = pd.concat([dflseg,newdf])
dflseg

dflseg.to_csv('lseg.csv')
