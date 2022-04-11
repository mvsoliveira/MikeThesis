
import numpy as np
import logging as lgr
import pandas as pd
lgr.basicConfig(level=lgr.INFO)
import glob
from natsort import natsorted
from Parser import parser
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

import pandas as pd
df= pd.read_csv("Portfolio.csv")

df['date net balance'] = pd.to_datetime(df['date net balance'], format='%Y-%m-%d')
df['date S&P 500'] = pd.to_datetime(df['date S&P 500'], format='%Y-%m-%d')
df['date BofA AAA bond'] = pd.to_datetime(df['date BofA AAA bond'], format='%Y-%m-%d')
df['date MSCI REIT'] = pd.to_datetime(df['date MSCI REIT'], format='%Y-%m-%d')
fig, ax = plt.subplots(1, 1)
df.plot(x="date net balance", y="net balance", ax=ax)
df.plot(x="date S&P 500", y="S&P 500", ax=ax)
df.plot(x="date BofA AAA bond", y="BofA AAA bond", ax=ax)
df.plot(x="date MSCI REIT", y="MSCI REIT", ax=ax)
ax.set_xlim([df["date net balance"].iloc[0], df["date net balance"].iloc[-1]])
ax.set_xlabel('Date')
ax.set_ylabel('Value (USD)')
#df.to_html("Portfolio.html")
print(df.dtypes)
plt.show()