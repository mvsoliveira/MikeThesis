
import numpy as np
import datetime as dt
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt


import pandas as pd
df = pd.read_csv("Percentchange.csv", usecols = ['SP','BofA','MCSI'])
#returns = df.loc(axis=0)['SP','BofA','MSCI']
print(df)

meanreturns= df.mean()
covmatrix= df.cov()

def portfolioperformance(weights, meanreturns, covmatrix):
    returns = np.sum(meanreturns*weights)*252
    std = np.sqrt(np.dot(weights.T, np.dot(covmatrix,weights)))*np.sqrt(252)
    return returns, std
weights= np.array([.03,.03,.04])
returns, std = portfolioperformance(weights, meanreturns, covmatrix)
print(round(returns*100,2), round(std*100,2))


