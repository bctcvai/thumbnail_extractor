#!/usr/bin/env python3

import argparse
import cv2
import os
import sys
import json

def exitOnBadPath(path):
    if not os.path.isfile(path):
        print(f"'{path}' is not valid")
        sys.exit(-1)

def processFile(mediaFp, localizationsFp, outputDir, nameAttribute):
    # Read in localizations
    with open(localizationsFp, 'r') as localizationsF:
        localizations=json.load(localizationsF)

    grouped_by_frame={}
    for localization in localizations:
        frame = localization['frame']
        if frame in grouped_by_frame:
            grouped_by_frame[frame].append(localization)
        else:
            grouped_by_frame[frame] = [localization]

    vid = cv2.VideoCapture(mediaFp)
    if cv2.__version__ >= "3.2.0":
        vid_len = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    else:
        vid_len = int(vid.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

    frame_num = 0
    while frame_num < vid_len:
        ok,image = vid.read()
        if not ok:
            raise RuntimeError("Failed to grab video frame")
        if frame_num in grouped_by_frame:
            print(f"Extracting localizations from {frame_num}")
            extractThumbnails(image, grouped_by_frame[frame_num],
                              outputDir,nameAttribute)
        frame_num += 1

def extractThumbnails(image, localizations, outputDir,nameAttribute):
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
    parser.add_argument("--localizations", "-l",
                        required=True,
                        type=str,
                        help="Input Localization File")
    parser.add_argument("--outputDir", "-o",
                        required=False,
                        default=os.getcwd())
    parser.add_argument("--nameAttribute", "-n",
                        required=False)

    args = parser.parse_args()

    exitOnBadPath(args.input)
    exitOnBadPath(args.localizations)

    sys.exit(processFile(args.input, args.localizations,
             args.outputDir, args.nameAttribute))
