#!/usr/bin/env python

import pytator
import os
import sys
import json
import pandas as pd

if __name__ == '__main__':
    media_ids = os.getenv('TATOR_MEDIA_IDS')
    media_ids = [int(m) for m in media_ids.split(',')]
    rest_svc = os.getenv('TATOR_API_SERVICE')
    work_dir = os.getenv('TATOR_WORK_DIR')
    token=os.getenv('TATOR_AUTH_TOKEN')
    project_id=os.getenv('TATOR_PROJECT_ID')
    tator=pytator.Tator(rest_svc, token, project_id)

    all_medias=tator.Media.all()
    all_types=tator.LocalizationType.all()
    box_type=None
    for typeObj in all_types:
        if typeObj['type']['dtype'] == 'box':
            box_type=typeObj
            break

    if box_type == None:
        print("No Box Types")
        sys.exit(-1)
    box_type_id = box_type['type']['id']

    work_filepath=os.path.join(work_dir, "work.csv")
    try:
        os.remove(work_filepath)
    except:
        pass

    for media in all_medias:
        if media['id'] in media_ids:
            media_localizations=tator.Localization.filter(
                {'media_id': media['id'],
                 'type': box_type_id})
            
            if media_localizations:
                print(f"Fetching {media['name']}")
                media_unique_name = f"{media['id']}_{media['name']}"
                media_filepath = os.path.join(work_dir,media_unique_name)
                tator.Media.downloadFile(media, media_filepath)
                json_filename = os.path.splitext(media_unique_name)[0] + '.json'
                json_filepath = os.path.join(work_dir, json_filename)
                with open(json_filepath, 'w') as json_file:
                    json.dump(media_localizations, json_file)
                data={'media': media_unique_name,
                      'localizations': json_filename}
                work_frame=pd.DataFrame(data=[data],
                                        columns=data.keys())
                work_frame.to_csv(work_filepath, index=False)
                
