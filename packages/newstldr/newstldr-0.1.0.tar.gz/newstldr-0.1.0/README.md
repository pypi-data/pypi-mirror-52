
# NewsTLDR

A Flasik extension to fetch and summarize the news. 

It provides an API `https://url/newstldr/`


You will also need **newstldr-admin**


### Requirements

- AWS Account for S3
- Google API Account for youtube

## Install

Add in Flasik application requirements.txt `newstldr`

## Config

```
    # NTLDR/Newsroom
    NTLDR_AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
    NTLDR_AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
    NTLDR_AWS_REGION_NAME = AWS_REGION_NAME
    NTLDR_IMAGES_STORAGE_PREFIX = "ntldr.imgs"
    NTLDR_SQS_MQ_NAME = "Newsroom"
    NTLDR_GOOGLE_API_KEY = GOOGLE_API_KEY
```

## __flasik__.py 

```
import newstldr.cli

projects = {
  "main": [
    "newstldr"
  ]
}
```

## Setup

`flasik news:setup`

## Run workers

To automatically import and process articles

### Import Posts
`flasik news:worker:import-posts`

### Run Task Q

`flasik news:worker:run-taskq`
