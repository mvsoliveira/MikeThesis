import pandas as pd
import logging as lgr
lgr.basicConfig(level=lgr.INFO)
import glob
from natsort import natsorted

class Parser(object):
    def read_xlsx(self, filepath):
        df = pd.read_excel(filepath)
        year = filepath.split(' ')[-1].split('-')[0]
        df['Year'] = year
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


