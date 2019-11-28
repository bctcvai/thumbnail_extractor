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
        pass
    elif mode == "state":
        pass
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

    exclude_rules=pipeline_args.get("exclude", None)

    # First write CSV header
    cols=['media', 'metadata']
    work_frame=pd.DataFrame(columns=cols)
    work_frame.to_csv(work_filepath, index=False)

    for media_id in media_ids:
        media = tator.Media.get(media_id)
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
            skip_file = True
            # Check to see if we need to process this file
            for element in metadata:
                if 'association' in element:
                    frame = element['association']['frame']
                else:
                    frame = element['frame']
                extracted_name = f"{element['id']}_{media['name']}_{frame}.png"
                extracted_element = tator.Media.filter({"name": extracted_name})
                if extracted_element is None or mode == 'localization_thumbnail':
                    skip_file = False
                    break

            if skip_file:
                print(f"Skipping {media['name']}")
            else:
                # Process exclude rules for thumbnail creation
                if exclude_rules:
                    print(f"Processing exclude rules {exclude_rules}")
                    for idx,el in enumerate(metadata):
                        for rule in exclude_rules:
                            if el.attributes[rule[0]] == rule[1]:
                                del metadata[idx]
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
