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

## Testing

`make test` unit test
`make docker_test` use tator test harness and invoke against server
