* Thumbnail extractor

Example pipeline for tator online. Can be used to extract png images of
annotated boxes from video and images. Uploads result to a new image.

** Required pipeline arguments:

imageTypeId : the type id to use for the thumbnail image

** sample config.json

```
  "TATOR_AUTH_TOKEN": "<TOKEN>",
  "TATOR_PROJECT_ID": "1",
  "TATOR_API_SERVICE": "https://debug.tatorapp.com/rest",
  "TATOR_MEDIA_IDS": "1",
  "TATOR_PIPELINE_ARGS" : "{\"imageTypeId\": 10}"
}
```

** testing

`make test` unit test
`make docker_test` use tator test harness and invoke against server
