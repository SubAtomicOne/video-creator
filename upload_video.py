import os
import random
import sys
import time
import argparse

import google.auth.exceptions
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from oauth2client.client import flow_from_clientsecrets
import httplib2

# Retry configuration
httplib2.RETRIES = 1
MAX_RETRIES = 10

RETRIABLE_EXCEPTIONS = (
    IOError, httplib2.HttpLib2Error
)

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

MISSING_CLIENT_SECRETS_MESSAGE = f"""
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   {os.path.abspath(CLIENT_SECRETS_FILE)}

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
"""

def get_authenticated_service(args):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)
    storage = Storage(f"{sys.argv[0]}-oauth2.json")
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                 http=credentials.authorize(httplib2.Http()))

def initialize_upload(youtube, options):
    tags = options.keywords.split(",") if options.keywords else None

    body = {
        "snippet": {
            "title": options.title,
            "description": options.description,
            "tags": tags,
            "categoryId": options.category
        },
        "status": {
            "privacyStatus": options.privacyStatus
        }
    }

    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
    )

    resumable_upload(insert_request)

def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0

    while response is None:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response:
                if 'id' in response:
                    print(f"Video id '{response['id']}' was successfully uploaded.")
                else:
                    sys.exit(f"The upload failed with an unexpected response: {response}")
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}"
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = f"A retriable error occurred: {e}"

        if error:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                sys.exit("No longer attempting to retry.")
            sleep_seconds = random.random() * (2 ** retry)
            print(f"Sleeping {sleep_seconds:.2f} seconds and then retrying...")
            time.sleep(sleep_seconds)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Video file to upload")
    parser.add_argument("--title", default="Test Title", help="Video title")
    parser.add_argument("--description", default="Test Description", help="Video description")
    parser.add_argument("--category", default="22", help="Numeric video category")
    parser.add_argument("--keywords", default="", help="Video keywords, comma separated")
    parser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES,
                        default="public", help="Video privacy status.")

    args = parser.parse_args()

    if not hasattr(args, 'logging_level'):
        args.logging_level = 'INFO'
    if not hasattr(args, 'noauth_local_webserver'):
        args.noauth_local_webserver = True 
    if not os.path.exists(args.file):
        sys.exit("Please specify a valid file using the --file= parameter.")

    youtube = get_authenticated_service(args)
    try:
        initialize_upload(youtube, args)
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
