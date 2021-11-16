import os
import re
import pandas as pd
import logging as lgr
lgr.basicConfig(level=lgr.INFO)
import glob
from natsort import natsorted
from Parser import parser

class Main(object):
    def __init__(self):
        self.raw_data = pd.DataFrame()
        filepaths = (natsorted(glob.glob('../../in/xlsx/*2019*.xlsx')))
        for filepath in filepaths:
            self.raw_data = self.raw_data.append(parser.read_xlsx(filepath),ignore_index=True)
        self.games = pd.DataFrame()
        for i in range(0,len(self.raw_data),2):
            row = pd.DataFrame()
            row['Visitor'] = [self.raw_data.at[i,'Team']]
            row['Home'] = [self.raw_data.at[i+1, 'Team']]
            row['Score'] = [self.raw_data.at[i, 'Final']- self.raw_data.at[i+1, 'Final']]
            self.games = self.games.append(row, ignore_index=True)

        self.raw_data.to_html('../../out/html/combined.html')
        self.games.to_html('../../out/html/games.html')

if __name__ == '__main__':
    main = Main()




