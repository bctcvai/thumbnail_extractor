#!/usr/bin/env python3

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
    pipeline_args_str = os.getenv('TATOR_PIPELINE_ARGS')
    if pipeline_args_str:
        pipeline_args = json.loads(pipeline_args_str)
    else:
        pipeline_args = {}
    tator=pytator.Tator(rest_svc, token, project_id)

    all_medias=tator.Media.all()

    mode=pipeline_args.get("mode", None)
    if mode == "localization_thumbnail" or mode == "localization_keyframe":
        # TODO: handle multiple state types
        local_types=tator.LocalizationType.all()
        frame_type=None
        for typeObj in local_types:
            if typeObj['type']['dtype'] == 'box':
                box_type=typeObj
                break
    elif mode == "state":
        state_types=tator.StateType.all()
        box_type=None
        for typeObj in state_types:
            if typeObj['type']['association'] == 'Frame':
                frame_type=typeObj
                break
    else:
        print("No mode specified to pipeline")
        sys.exit(-1)

    type_id = pipeline_args.get("type_id", None)
    if type_id == None:
        print("No type id specified.")
        sys.exit(-1)

    work_filepath=os.path.join(work_dir, "work.csv")
    try:
        os.remove(work_filepath)
    except:
        pass

    # First write CSV header
    cols=['media', 'metadata']
    work_frame=pd.DataFrame(columns=cols)
    work_frame.to_csv(work_filepath, index=False)

    for media in all_medias:
        if media['id'] in media_ids:
            media_unique_name = f"{media['id']}_{media['name']}"
            media_filepath = os.path.join(work_dir,media_unique_name)
            data={'media': media_unique_name}

            if mode == "localization_thumbnail" or mode == "localization_keyframe":
                metadata=tator.Localization.filter(
                    {'media_id': media['id'],
                     'type': type_id})
            elif mode == "state":
                metadata=tator.State.filter(
                    {'media_id': media['id'],
                     'type': type_id})

            if metadata:
                print(f"Fetching {media['name']}")
                tator.Media.downloadFile(media, media_filepath)
                json_filename = os.path.splitext(media_unique_name)[0] + '.json'
                json_filepath = os.path.join(work_dir, json_filename)
                with open(json_filepath, 'w') as json_file:
                    json.dump(metadata, json_file)
                    data.update({'metadata': json_filename})

                work_frame=pd.DataFrame(data=[data],
                                    columns=cols)
                work_frame.to_csv(work_filepath, index=False, header=False, mode='a')
