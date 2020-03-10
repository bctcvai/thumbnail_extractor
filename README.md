# Thumbnail extractor

Example pipeline for tator online. Can be used to extract png images of
annotated boxes from video and images. Uploads result to a new image.

## Required pipeline arguments:

imageTypeId : the type id to use for the thumbnail image

## Sample config.json

`config.json` can be used with the `tator_testHarness.py` script

`tator_testHarness.py config.json tator/setup.py`

```
  "TATOR_AUTH_TOKEN": "<TOKEN>",
  "TATOR_PROJECT_ID": "1",
  "TATOR_API_SERVICE": "https://debug.tatorapp.com/rest",
  "TATOR_MEDIA_IDS": "1",
  "TATOR_PIPELINE_ARGS" : "{\"imageTypeId\": 10}"
}
```

## Example from Tator Online

The arguments attribute in an Algorithm model could look like the following:
```
{"mode": "localization_keyframe",
"type_id": 48,
"imageTypeId": 50,
"dest_section": "Training Box Extracts"}
```

Where:

`mode`: One of

     - `localization_keyframe`: Extracts whole frame duplicates localizations in new image

     - `localization_thumbnail`: Extracts content of localization box and applies attributes as media attributes to the resultant image.

     - `state`: Same as `localization_keyframe` but with `State` types.

`type_id`: The underlying type of the object to base extractions off of.

`imageTypeId`: The destination image type.

`dest_section`: The name of the section to place the extracted imagery.

## Testing

`make test` unit test
`make docker_test` use tator test harness and invoke against server
