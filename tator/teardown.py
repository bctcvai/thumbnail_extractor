#!/usr/bin/env python3

import pytator
import json
import os
import sys

def uploadThumbnails(tator, dest_tator, mode, thumbnail_type_id, directory, sectionName):
    for dir_element in os.listdir(directory):
        full_path=os.path.join(directory, dir_element)
        original_media_id = os.path.basename(directory).split('_')[0]
        localization_id_or_frame=int(os.path.splitext(dir_element)[0])
        md5=pytator.md5sum.md5_sum(full_path)
        media=dest_tator.Media.byMd5(md5)
        if not media:
            dest_tator.Media.uploadFile(thumbnail_type_id,
                                        full_path,
                                        waitForTranscode=True,
                                        progressBars=False,
                                        md5=md5,
                                        section=sectionName)
            media=tator.Media.byMd5(md5)
        else:
            print("Frame Extraction Media found in db.")

        if mode == "state" or mode == "localization_keyframe":
            print("processing localizations/states from video into image")
            frame = localization_id_or_frame
            # Iterate over each state type that belongs to the destination
            # image type.
            state_types=dest_tator.StateType.filter({'media_id':media['id']})
            if state_types is None:
                state_types=[]
            for state_type in state_types:
                type_id = state_type['type']['id']
                states=tator.State.filter({'type': type_id,
                                        'media_id' : original_media_id})
                if states is None:
                    continue
                print(f"importing {state_type['type']['name']}")
                for entry in states:
                    if entry['frame'] != frame:
                        continue
                    obj={'media_ids': media['id'],
                         'frame': 0, #images are always frame 0
                         'type' : state_type['type']['id']}
                    obj.update(entry['attributes'])
                    tator.State.new(obj)

            #Clone types from localizations
            localization_types=dest_tator.LocalizationType.filter({'media_id':
                                                            media['id']})
            if localization_types is None:
                localization_types=[]
            for localization_type in localization_types:
                type_id = localization_type['type']['id']
                dtype = localization_type['type']['dtype']
                print(f"importing {localization_type['type']['name']} objects")
                localizations=tator.Localization.filter({'type': type_id,
                                                         'media_id' : original_media_id})
                if localizations is None:
                    print(f"No localizations found on {frame}")
                    continue

                for entry in localizations:
                    if entry['frame'] != frame:
                        continue
                    obj={'media_id': media['id'],
                         'frame': 0, #images are always frame 0
                         'type' : localization_type['type']['id']}
                    obj.update(entry['attributes'])
                    if dtype == 'box':
                        obj['x'] = entry['x']
                        obj['y'] = entry['y']
                        obj['height'] = entry['height']
                        obj['width'] = entry['width']
                    elif dtype == 'line':
                        obj['x0'] = entry['x0']
                        obj['y0'] = entry['y0']
                        obj['x1'] = entry['x1']
                        obj['y1'] = entry['y1']
                    elif dtype == 'dot':
                        obj['x'] = entry['x']
                        obj['y'] = entry['y']
                    tator.Localization.new(obj)
        elif mode == "localization_thumbnail":
            localization_id = localization_id_or_frame
            localization=tator.Localization.get(localization_id)
            media_attrs=media['attributes']
            media_attrs.update(localization['attributes'])
            tator.Media.applyAttribute(media['id'], media_attrs)
            tator.Localization.update(localization_id,
                                      {"thumbnail_image": media['id']})

if __name__ == '__main__':
    rest_svc = os.getenv('TATOR_API_SERVICE')
    work_dir = os.getenv('TATOR_WORK_DIR')
    token = os.getenv('TATOR_AUTH_TOKEN')
    project_id = os.getenv('TATOR_PROJECT_ID')
    pipeline_args_str = os.getenv('TATOR_PIPELINE_ARGS')
    if pipeline_args_str:
        pipeline_args = json.loads(pipeline_args_str)
    else:
        print("ERROR: No pipeline arguments specified!")
        sys.exit(-1)
    thumbnail_type_id = pipeline_args['imageTypeId']
    dest_project_id = pipeline_args.get('destProject', project_id)
    mode = pipeline_args.get('mode', None)

    tator = pytator.Tator(rest_svc, token, project_id)
    dest_tator = pytator.Tator(rest_svc, token, dest_project_id)
    dest_section = pipeline_args.get("dest_section", "Extracted Frames")
    for dir_element in os.listdir(work_dir):
        full_path=os.path.join(work_dir, dir_element)
        if os.path.isdir(full_path):
            uploadThumbnails(tator, dest_tator, mode, thumbnail_type_id, full_path, dest_section)
