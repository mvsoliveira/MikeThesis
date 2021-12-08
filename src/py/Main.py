
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
        self.raw_data = pd.DataFrame()
        filepaths = (natsorted(glob.glob('../../in/xlsx/*.xlsx')))
        for filepath in filepaths:
            self.raw_data = self.raw_data.append(parser.read_xlsx(filepath),ignore_index=True)
        self.games = pd.DataFrame(columns=['Visitor', 'Home'])
        for i in range(0,len(self.raw_data),2):
            row = pd.DataFrame()
            self.raw_data.at[i, 'Score'] = self.raw_data.at[i, 'Final']- self.raw_data.at[i+1, 'Final']
            self.raw_data.at[i+1, 'Score'] = self.raw_data.at[i+1, 'Final'] - self.raw_data.at[i, 'Final']
            row['Year'] = [self.raw_data.at[i, 'Year']]
            row['Visitor'] = [self.raw_data.at[i,'Team']]
            row['Home'] = [self.raw_data.at[i+1, 'Team']]
            row['Score'] = [self.raw_data.at[i, 'Final']- self.raw_data.at[i+1, 'Final']]
            row['Visitor Open'] = [self.raw_data.at[i, 'Open']]
            row['Visitor Close'] = [self.raw_data.at[i, 'Close']]
            row['Home Open'] = [self.raw_data.at[i+1, 'Open']]
            row['Home Close'] = [self.raw_data.at[i+1, 'Close']]
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
                for i in range(self.raw_data['Contract Momentum']):
                    if i >= 15:
                        if self.raw_data['Score'] > 0:
                    self.raw_data['Long Strategy'] = 0
                            if self.raw_data['Open'] < 0:
                        self.raw_data['Long Strategy'] = -100
                                self.raw_data['Long Strategy'] = (1 - (100 / self.raw_data['Open']))*100
                            self.raw_data['Long Strategy'] = ((self.raw_data['Open'] / 100) + 1)*100


#Plotting Contract Momentum
            lgr.info('Generating plot')
            plt.hist(self.raw_data['Contract Momentum'], color='blue', edgecolor='black')
            plt.title('Histogram of Contract Momentum')
            plt.xlabel('Contract Momentum')
            plt.ylabel('Strength of Momentum')
            plt.show()


        self.raw_data.to_html('../../out/html/combined.html')
        self.games.to_html('../../out/html/games.html')
        #self.raw_data.to_excel(r'/Users/michaelvollmin/Desktop/combined.xlsx')
if __name__ == '__main__':
    main = Main()




