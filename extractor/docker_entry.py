#!/usr/bin/env python3

import os
import pandas as pd
import extractor
import json

if __name__=="__main__":
    work_dir = os.getenv('TATOR_WORK_DIR')
    pipeline_args_str = os.getenv('TATOR_PIPELINE_ARGS')
    if pipeline_args_str:
        pipeline_args = json.loads(pipeline_args_str)
    else:
        pipeline_args = {}
    work_filepath=os.path.join(work_dir, "work.csv")
    work_data=pd.read_csv(work_filepath)
    for idx,work in work_data.iterrows():
        image_workpath=os.path.join(work_dir,
                                    os.path.splitext(work['media'])[0])
        try:
            os.mkdir(image_workpath)
        except:
            pass
        extractor.processFile(os.path.join(work_dir,work['media']),
                              os.path.join(work_dir,work['localizations']),
                              image_workpath)
