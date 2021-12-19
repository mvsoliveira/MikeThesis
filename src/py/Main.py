
import numpy as np
import pandas as pd
import logging as lgr
import logging as lgr
import numpy as np
import pandas as pd
lgr.basicConfig(level=lgr.INFO)
import glob
from natsort import natsorted
from Parser import parser
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
#import seaborn as sns

class Main(object):
    def __init__(self):
        self.min_games = 8
        self.portifolio = 1000
        self.bet_ratio = 0.1
        self.raw_data = pd.DataFrame()
        filepaths = (natsorted(glob.glob('../../in/xlsx/*2019*.xlsx')))
        for filepath in filepaths:
            self.raw_data = self.raw_data.append(parser.read_xlsx(filepath),ignore_index=True)
        for i in range(0,len(self.raw_data),2):
            self.raw_data.at[i, 'Score'] = self.raw_data.at[i, 'Final']- self.raw_data.at[i+1, 'Final']
            self.raw_data.at[i+1, 'Score'] = self.raw_data.at[i+1, 'Final'] - self.raw_data.at[i, 'Final']
            for k in range(2):
                past_data = self.raw_data[0:i+k]
                games = past_data[past_data['Team'] == self.raw_data.at[i+k,'Team']]
                if len(games) >= self.min_games:
                    self.raw_data.at[i+k, 'Momentum'] = sum(games['Score'][-self.min_games:])
                else:
                    self.raw_data.at[i+k, 'Momentum'] = np.NaN
                self.raw_data.at[i, 'Contract Momentum'] = self.raw_data.at[i, 'Momentum'] - self.raw_data.at[i+1, 'Momentum']
                self.raw_data.at[i+1, 'Contract Momentum'] = self.raw_data.at[i+1, 'Momentum'] - self.raw_data.at[i, 'Momentum']
###Attempt to make Lng strategy column (Using bets of $100)
        net_balance = self.portifolio
        for i in range(len(self.raw_data)):
            self.bet_value = self.bet_ratio * net_balance
            if self.raw_data.at[i,'Contract Momentum'] >= 15:
                if self.raw_data.at[i,'Score'] > 0:
                    if self.raw_data.at[i,'Open'] < 0:
                        bet_balance = ((1 - (100 / self.raw_data.at[i,'Open'])) * self.bet_value) -self.bet_value
                    else:
                        bet_balance = (((self.raw_data.at[i,'Open'] / 100) + 1) * self.bet_value) -self.bet_value
                else:
                    bet_balance = -self.bet_value
            else:
                bet_balance = 0
            self.raw_data.at[i,'Long Strategy'] = bet_balance
            net_balance = net_balance + bet_balance
            self.raw_data.at[i, 'Net Balance'] = net_balance



#Plotting Contract Momentum
        lgr.info('Generating plot')
        plt.hist(self.raw_data['Contract Momentum'], color='blue', edgecolor='black')
        plt.title('Histogram of Contract Momentum')
        plt.xlabel('Contract Momentum')
        plt.ylabel('Strength of Momentum')
        plt.show()

        lgr.info('Generating plot')
        plt.plot(self.raw_data.Net_balance)
        plt.title('Line Chart starting with $1000')
        plt.xlabel('Date')
        plt.ylabel('Net Balance')
        plt.show()

        self.raw_data.to_html('../../out/html/combined.html')
        #self.raw_data.to_excel(r'/Users/michaelvollmin/Desktop/combined.xlsx')
if __name__ == '__main__':
    main = Main()




