#!/usr/bin/env python3

import argparse
import cv2
import os
import sys
import json
import numpy as np

def exitOnBadPath(path):
    if not os.path.isfile(path):
        print(f"'{path}' is not valid")
        sys.exit(-1)

def processFile(mediaFp, mode, metadataFp, outputDir):
    # Read in metadata
    with open(metadataFp, 'r') as metadataF:
        metadata=json.load(metadataF)

    grouped_by_frame={}
    if mode == "state":
        for entry in metadata:
            frame = entry['association']['frame']
            if frame in grouped_by_frame:
                grouped_by_frame[frame].append(entry)
            else:
                grouped_by_frame[frame] = [entry]

    elif mode == "localization_keyframe":
        for entry in metadata:
            frame = entry['frame']
            if frame in grouped_by_frame:
                grouped_by_frame[frame].append(entry)
            else:
                grouped_by_frame[frame] = [entry]
    else:
        for entry in metadata:
            if entry['thumbnail_image']:
                print("Skipping entry with valid thumbnail")
                continue
            frame = entry['frame']
            if frame in grouped_by_frame:
                grouped_by_frame[frame].append(entry)
            else:
                grouped_by_frame[frame] = [entry]

    vid = cv2.VideoCapture(mediaFp)
    if cv2.__version__ >= "3.2.0":
        vid_len = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    else:
        vid_len = int(vid.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

    frame_num = 0
    if len(grouped_by_frame.keys()) > 0:
        max_frame = np.max(list(grouped_by_frame.keys()))
    else:
        print("Nothing to extract")
        max_frame = 0
    while frame_num <= max_frame:
        ok,image = vid.read()
        if not ok:
            raise RuntimeError("Failed to grab video frame")
        else:
            if frame_num in grouped_by_frame:
                print(f"Extracting metadata from {frame_num}")
                if mode == 'state' or mode == 'localization_keyframe':
                    output_name = os.path.basename(mediaFp)
                    output_name += f"_{frame_num}.png"
                    output_fp = os.path.join(outputDir, output_name)
                    cv2.imwrite(output_fp, image)
                else:
                    extractThumbnails(image, grouped_by_frame[frame_num],
                                      outputDir)
        frame_num += 1

def extractThumbnails(image, localizations, outputDir):
    for localization in localizations:
        output_name = f"{localization['id']}.png"
        output_fp = os.path.join(outputDir, output_name)

        # Now get the image data from the image
        height=image.shape[0]
        width=image.shape[1]

        thumb_height = int(height * localization['height'])
        thumb_width = int(width * localization['width'])
        thumb_y = int(height * localization['y'])
        thumb_x = int(width * localization['x'])

        thumbnail = image[thumb_y:thumb_y+thumb_height,
                          thumb_x:thumb_x+thumb_width,
                          :];
        cv2.imwrite(output_fp, thumbnail)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Thumbnail Extractor")
    parser.add_argument("--input", "-i",
                        required=True,
                        type=str,
                        help="Input Media File")
    parser.add_argument("--metadata", "-m",
                        required=True,
                        type=str,
                        help="Input Metadata File")
    parser.add_argument("--mode",
                        required=True)
    parser.add_argument("--outputDir", "-o",
                        required=False,
                        default=os.getcwd())

    args = parser.parse_args()

    exitOnBadPath(args.input)
    exitOnBadPath(args.metadata)

    sys.exit(processFile(args.input,
                         args.mode,
                         args.metadata,
                         args.outputDir))
