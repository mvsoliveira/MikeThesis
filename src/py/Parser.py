import pandas as pd
import logging as lgr
lgr.basicConfig(level=lgr.INFO)
import glob
from natsort import natsorted

class Parser(object):
    def read_xlsx(self, filepath):
        df = pd.read_excel(filepath)
        year = filepath.split(' ')[-1].split('-')[0]
        year_array = [int(year), int(year)+1]
        year_crossed = 0
        for i in range(len(df)):
            if "{0:04d}".format(int(df.at[i,'Date']))[0:2] == "01":
                year_crossed = 1
            df.at[i, 'Year'] = year_array[year_crossed]
        return df

    def save_html(self,df,filepath):
        df.to_html(filepath)



parser = Parser()

if __name__ == '__main__':
    filepaths = (natsorted(glob.glob('../../in/xlsx/*.xlsx')))
    for filepath in filepaths:
        df = parser.read_xlsx(filepath)
        filepath = filepath.replace('in', 'out').replace('xlsx', 'html')
        parser.save_html(df, filepath)


