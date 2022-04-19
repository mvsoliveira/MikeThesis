
import numpy as np
import datetime as dt
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import scipy.optimize as sc


import pandas as pd
df = pd.read_csv("Percentchange.csv", usecols = ['SP','BofA','MCSI'])
#returns = df.loc(axis=0)['SP','BofA','MSCI']
#print(df)
#stocklist= ['SP','BofA','MCSI']
#stocks= (stock+ '.AX' for stock in stocklist)
meanreturns= df.mean()
meanreturnslist= [asset for asset in meanreturns]
numAssets= len(meanreturns)
weights= np.array([.03,.03,.04])

#print(meanreturnslist)

for asset in meanreturns:
    print(asset)

covmatrix= df.cov()

#print(meanreturns)

def portfolioperformance(weights, meanreturns, covmatrix):
    returns = np.sum(meanreturns*weights)*252
    std = np.sqrt(np.dot(weights.T, np.dot(covmatrix,weights)))*np.sqrt(252)
    return returns, std



weights= np.array([.03,.03,.04])
returns, std = portfolioperformance(weights, meanreturns, covmatrix)
print(round(returns*100,2), round(std*100,2))


def negativeSR(weights, meanreturns, covmatrix, riskFreeRate = 0):
    pReturns, pStd = portfolioperformance(weights, meanreturns, covmatrix)
    return - (pReturns - riskFreeRate)/pStd

def maxSR(meanreturns, covmatrix, riskFreeRate = 0, constraintSet=(0,1)):
    "Minimize the negative SR, by altering the weights of the portfolio"
    numAssets = len(meanreturns)
    args = (meanreturns, covmatrix, riskFreeRate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = constraintSet
    bounds = tuple(bound for asset in range(numAssets))
    result = sc.minimize(negativeSR, numAssets*[1./numAssets], args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints)
    return result


result = maxSR(meanreturns, covmatrix)
maxSR, maxWeights= result['fun'], result['x']
print(maxSR, maxWeights)


def portfolioVariance(weights, meanreturns, covmatrix):
    return portfolioperformance(weights, meanreturns, covmatrix)[1]


def minimizeVariance(meanreturns, covmatrix, constraintSet=(0,1)):
    """Minimize the portfolio variance by altering the
     weights/allocation of assets in the portfolio"""
    numAssets = len(meanreturnslist)
    args = (meanreturns, covmatrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = constraintSet
    bounds = tuple(bound for asset in range(numAssets))
    result = sc.minimize(portfolioVariance, numAssets*[1./numAssets], args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints)
    return result


minVarresult= minimizeVariance(meanreturns, covmatrix)
minVar, minVarWeights= minVarresult['fun'], minVarresult['x']
print(minVarresult, minVarresult)


def portfolioReturn(weights, meanreturns, covmatrix):
    return portfolioperformance(weights, meanreturns, covmatrix)[0]


def efficientOpt(meanreturns, covmatrix, returnTarget, constraintSet=(0,1)):
    """For each returnTarget, we want to optimise the portfolio for min variance"""
    numAssets = meanreturns
    args = (meanreturns, covmatrix)

    constraints = ({'type':'eq', 'fun': lambda x: portfolioReturn(x, meanreturns, covmatrix) - returnTarget},
                    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = constraintSet
    bounds = tuple(bound for asset in range(numAssets))
    effOpt = sc.minimize(portfolioVariance, numAssets*[1./numAssets], args=args, method = 'SLSQP', bounds=bounds, constraints=constraints)
    return effOpt


def calculatedResults(meanreturns, covmatrix, riskFreeRate=0, constraintSet=(0, 1)):
    """Read in mean, cov matrix, and other financial information
        Output, Max SR , Min Volatility, efficient frontier """
    # Max Sharpe Ratio Portfolio
    maxSR_Portfolio = maxSR(meanreturns, covmatrix)
    maxSR_returns, maxSR_std = portfolioperformance(maxSR_Portfolio['x'], meanreturns, covmatrix)
    maxSR_returns, maxSR_std = round(maxSR_returns * 100, 2), round(maxSR_std * 100, 2)
    maxSR_allocation = pd.DataFrame(maxSR_Portfolio['x'], index=meanreturns.index, columns=['allocation'])
    maxSR_allocation.allocation = [round(i * 100, 0) for i in maxSR_allocation.allocation]

    # Min Volatility Portfolio
    minVol_Portfolio = minimizeVariance(meanreturns, covmatrix)
    minVol_returns, minVol_std = portfolioperformance(minVol_Portfolio['x'], meanreturns, covmatrix)
    minVol_returns, minVol_std = round(minVol_returns * 100, 2), round(minVol_std * 100, 2)
    minVol_allocation = pd.DataFrame(minVol_Portfolio['x'], index=meanreturns.index, columns=['allocation'])
    minVol_allocation.allocation = [round(i * 100, 0) for i in minVol_allocation.allocation]

    # Efficient Frontier
    efficientList = []
    targetReturns = np.linspace(minVol_returns, maxSR_returns, 20)
    for target in targetReturns:
        efficientList.append(efficientOpt(meanreturns, covmatrix, target)['fun'])

    return maxSR_returns, maxSR_std, maxSR_allocation, minVol_returns, minVol_std, minVol_allocation, efficientList


print(calculatedResults(meanreturns, covmatrix))
