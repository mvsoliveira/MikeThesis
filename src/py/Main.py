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
        df = pd.DataFrame()
        filepaths = (natsorted(glob.glob('../../in/xlsx/*.xlsx')))
        for filepath in filepaths:
            df = df.append(parser.read_xlsx(filepath),ignore_index=True)
        df.to_html('../../out/html/combined.html')

if __name__ == '__main__':
    main = Main()




