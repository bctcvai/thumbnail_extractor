#!/usr/bin/env python3

import os
import pandas as pd

if __name__=="__main__":
    work_dir = os.getenv('TATOR_WORK_DIR')
    work_filepath=os.path.join(work_dir, "work.csv")
    work_data=pd.read_csv(work_filepath)
    for idx,work in work_data.iterrows():
        print(work)
