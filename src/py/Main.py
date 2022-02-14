
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
#import seaborn as sns

class Main(object):
    def __init__(self):
        global No_Vig_Open
        self.min_games = 8
        self.portfolio = 1000
        self.bet_ratio_risky = 0.5
        self.bet_ratio_moderate = 0.3
        self.bet_ratio_conservative = 0.1
        self.raw_data = pd.DataFrame()
        filepaths = (natsorted(glob.glob('../../in/xlsx/*.xlsx')))
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
 ####Calculating implied probability, and vig
        #net_balance = self.portfolio
        for i in range(len(self.raw_data)):
            print(self.raw_data.at[i,'Date'], self.raw_data.at[i,'Year'])
            self.raw_data.at[i,'good_date'] = date(day=int("{0:04d}".format(self.raw_data.at[i,'Date'])[2:4]), month=int("{0:04d}".format(self.raw_data.at[i,'Date'])[0:2]), year=int(self.raw_data.at[i,'Year']))
            if self.raw_data.at[i,'Open'] < 0 :
                risk_open = self.raw_data.at[i, 'Open'] * -1
                _return_open = risk_open + 100
            else:
                risk_open = 100
                _return_open = risk_open + self.raw_data.at[i, 'Open']
            if self.raw_data.at[i,'Close'] < 0:
                risk_close = self.raw_data.at[i, 'Close'] * -1
                _return_close = risk_close + 100
            else:
                risk_close = 100
                _return_close = risk_close + self.raw_data.at[i, 'Close']
            implied_probability_open = risk_open / _return_open
            implied_probability_close = risk_close / _return_close
            self.raw_data.at[i, 'Implied Probability Open'] = implied_probability_open
            self.raw_data.at[i, 'Implied Probability Close'] = implied_probability_close
        for i in range(0, len(self.raw_data), 2):
            self.raw_data.at[i, 'Total Implied Open'] = self.raw_data.at[i, 'Implied Probability Open'] + self.raw_data.at[i + 1, 'Implied Probability Open']
            self.raw_data.at[i + 1, 'Total Implied Open'] = self.raw_data.at[i + 1, 'Implied Probability Open'] + self.raw_data.at[i, 'Implied Probability Open']
            self.raw_data.at[i, 'Total Implied Close'] = self.raw_data.at[i, 'Implied Probability Close'] + self.raw_data.at[i+1, 'Implied Probability Close']
            self.raw_data.at[i+1, 'Total Implied Close'] = self.raw_data.at[i+1, 'Implied Probability Close'] + self.raw_data.at[i, 'Implied Probability Close']
        for i in range(len(self.raw_data)):
            actual_probability_open = self.raw_data.at[i, 'Implied Probability Open'] / self.raw_data.at[i, 'Total Implied Open']
            actual_probability_close = self.raw_data.at[i, 'Implied Probability Close'] / self.raw_data.at[i, 'Total Implied Close']
            if self.raw_data.at[i, 'Open'] < 0:
               No_Vig_Open = -1 * (actual_probability_open / (1 - actual_probability_open)) * 100
            else:
                No_Vig_Open = ((1 - actual_probability_open) / actual_probability_open) * 100
            if self.raw_data.at[i, 'Close'] < 0:
                No_Vig_Close = -1 * (actual_probability_close / (1 - actual_probability_close)) * 100
            else:
                No_Vig_Close = ((1 - actual_probability_close) / actual_probability_close) * 100
            self.raw_data.at[i, 'Vig-Less Open'] = No_Vig_Open
            self.raw_data.at[i, 'Vig-Less Close'] = No_Vig_Close
            self.raw_data.at[i, 'Actual Prob open']= actual_probability_open
            self.raw_data.at[i, 'Actual Prob close'] = actual_probability_close

        net_balance = self.portfolio
        for i in range(len(self.raw_data)):
#### Making bet value a function of Momentum
            if self.raw_data.at[i,'Momentum'] > 0 and -5 <= self.raw_data.at[i,'Contract Momentum'] <= 5:
                self.short_bet_value = self.bet_ratio_risky * self.portfolio
                self.long_bet_value = self.bet_ratio_risky * self.portfolio
            elif self.raw_data.at[i,'Contract Momentum'] >= 15 and self.raw_data.at[i,'Momentum'] < 0:
                self.short_bet_value = self.bet_ratio_moderate * self.portfolio
                self.long_bet_value = self.bet_ratio_conservative * self.portfolio
            elif self.raw_data.at[i,'Contract Momentum'] >= 10 and self.raw_data.at[i,'Momentum'] >= 10:
                self.short_bet_value = self.bet_ratio_risky * self.portfolio
                self.long_bet_value = self.bet_ratio_risky * self.portfolio
            elif self.raw_data.at[i,'Contract Momentum'] > 0 and self.raw_data.at[i,'VH'] == "H" and self.raw_data.at[i,'Momentum'] >= 0 :
                self.short_bet_value = self.bet_ratio_risky * self.portfolio
                self.long_bet_value = self.bet_ratio_risky * self.portfolio
            elif self.raw_data.at[i, 'Contract Momentum'] >= 10 and self.raw_data.at[i,'Momentum'] >= self.raw_data.at[i, 'Contract Momentum']/2 :
                self.short_bet_value = self.bet_ratio_risky * self.portfolio
                self.long_bet_value = self.bet_ratio_risky * self.portfolio
            elif self.raw_data.at[i, 'Contract Momentum'] <= -10 and self.raw_data.at[i,'Momentum'] < 5 and self.raw_data.at[i,'VH'] == "V":
                self.short_bet_value = 0 * self.portfolio
                self.long_bet_value = self.bet_ratio_risky * self.portfolio
            elif self.raw_data.at[i, 'Momentum'] > self.raw_data.at[i, 'Contract Momentum'] and self.raw_data.at[i, 'VH'] == "V":
                self.long_bet_value = self.bet_ratio_moderate * self.portfolio
            else:
                self.short_bet_value = self.bet_ratio_risky * self.portfolio
                self.long_bet_value = self.bet_ratio_conservative * self.portfolio
###Creating Long Position
            if self.raw_data.at[i,'Contract Momentum'] >= 10:
                if self.raw_data.at[i,'Score'] > 0:
                    if self.raw_data.at[i, 'Open'] < 0:
                        bet_balance = self.long_bet_value/(-1* self.raw_data.at[i, 'Open']/100)
                    else:
                        bet_balance = (((self.raw_data.at[i, 'Open'] / 100) + 1) * self.long_bet_value) - self.long_bet_value
                else:
                    if self.raw_data.at[i, 'Open'] < 0:
                        bet_balance = - self.long_bet_value
                    else:
                        bet_balance = - self.long_bet_value
                self.raw_data.at[i, 'Long Strategy'] = bet_balance
                self.raw_data.at[i, 'Short Strategy'] = 0
    ###Creating Short Position
            elif self.raw_data.at[i,'Contract Momentum'] <= -10 :
                if self.raw_data.at[i,'Score'] > 0:
                    if self.raw_data.at[i, 'Close'] > 0:
                        bet_balance = (((self.raw_data.at[i, 'Close'] / 100) + 1) * self.short_bet_value) - self.short_bet_value
                    else:
                        bet_balance = self.short_bet_value/(-1* self.raw_data.at[i, 'Close']/100)
                else:
                    if self.raw_data.at[i, 'Close'] > 0:
                        bet_balance = - self.short_bet_value
                    else:
                        bet_balance = - self.short_bet_value
                self.raw_data.at[i, 'Short Strategy'] = bet_balance
                self.raw_data.at[i, 'Long Strategy'] = 0
            else:
                self.raw_data.at[i, 'Short Strategy'] = 0
                self.raw_data.at[i, 'Long Strategy'] = 0
                bet_balance = 0
            net_balance = net_balance + bet_balance
            self.raw_data.at[i,'Net Balance'] = net_balance


#Plotting Contract Momentum
        #lgr.info('Generating plot')
        #plt.hist(self.raw_data['Contract Momentum'], color='blue', edgecolor='black')
        #plt.title('Histogram of Contract Momentum')
        #plt.xlabel('Contract Momentum')
        #plt.ylabel('Strength of Momentum')
        #plt.show()

        lgr.info('Generating plot')
        plt.plot(self.raw_data['good_date'], self.raw_data['Net Balance'])
        plt.title('Long-Short Strategy, with Transaction Costs, using Contract Momentum +15/-5, betvalue as a function of momentum +-15 growth of  $1000')
        plt.xlabel('Time 2007-2021')
        plt.ylabel('Net Balance')
        plt.show()


        self.raw_data[['good_date','Date', 'VH', 'Team','Final', 'Open','Close', 'Year', 'Score', 'Momentum', 'Contract Momentum','Implied Probability Open', 'Actual Prob open', 'Implied Probability Close', 'Actual Prob open', 'Total Implied Open','Total Implied Close','Vig-Less Open', 'Vig-Less Close','Long Strategy', 'Short Strategy', 'Net Balance']].to_html('../../out/html/combined.html')
        #self.raw_data.to_excel(r'/Users/michaelvollmin/Desktop/combined.xlsx')
if __name__ == '__main__':
    main = Main()




