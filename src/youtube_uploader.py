
import os
import random
import sys
import time
import json
from pathlib import Path
import httplib2

from apiclient.discovery import build  # pylint: disable=import-error
from apiclient.errors import HttpError  # pylint: disable=import-error
from apiclient.http import MediaFileUpload  # pylint: disable=import-error, unknown-option-value
from oauth2client.client import flow_from_clientsecrets  # pylint: disable=import-error
from oauth2client.file import Storage  # pylint: disable=import-error
from oauth2client.tools import run_flow  # pylint: disable=import-error

# Determine parent path of repository
parent_dir = Path.cwd()
print(parent_dir)

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.cloud.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = parent_dir / "data/client_secrets.json"

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = f"""
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

{CLIENT_SECRETS_FILE}

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
"""

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_authenticated_service():
    '''The function `get_authenticated_service` returns an authenticated YouTube API service object.
    
    Returns
    -------
        a built YouTube API service object that is authenticated with the provided credentials.
    
    '''

    flow = flow_from_clientsecrets(
        CLIENT_SECRETS_FILE,
        scope=YOUTUBE_UPLOAD_SCOPE,
        message=MISSING_CLIENT_SECRETS_MESSAGE,
    )

    storage = Storage(parent_dir / "data/main_uploader-oauth2.json")
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)

    return build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        http=credentials.authorize(httplib2.Http()),
    )

def initialize_upload(yt, video_args):
    '''The function `initialize_upload` initializes the upload of a video to YouTube using the YouTube Data
    API.
    
    Parameters
    ----------
    yt
        The `yt` parameter is an instance of the YouTube API client that is used to make requests to the
    YouTube API.
    video_args
        The `video_args` parameter is a dictionary that contains the following information:
    
    '''

    tags = None
    if video_args["hashtags"]:
        tags = video_args["hashtags"].split(",")

    body = dict(
        snippet=dict(
            title=video_args["video_title"],
            description=video_args["description"],
            tags=tags,
            categoryId=video_args["category"],
        ),
        status=dict(privacyStatus=video_args["privacy_status"]),
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = yt.videos().insert(
        part=",".join(body.keys()),
        body=body,
        # The chunksize parameter specifies the size of each chunk of data, in
        # bytes, that will be uploaded at a time. Set a higher value for
        # reliable connections as fewer chunks lead to faster uploads. Set a lower
        # value for better recovery on less reliable connections.
        #
        # Setting "chunksize" equal to -1 in the code below means that the entire
        # file will be uploaded in a single HTTP request. (If the upload fails,
        # it will still be retried where it left off.) This is usually a best
        # practice, but if you're using Python older than 2.6 or if you're
        # running on App Engine, you should set the chunksize to something like
        # 1024 * 1024 (1 megabyte).
        media_body=MediaFileUpload(video_args["video_file"], chunksize=-1, resumable=True),
    )

    resumable_upload(insert_request)


# This method implements an exponential backoff strategy to resume a
# failed upload.


def resumable_upload(insert_request):
    '''The function `resumable_upload` handles the resumable upload of a file, with retry logic in case of
    errors.
    
    Parameters
    ----------
    insert_request
        The `insert_request` parameter is an object that represents the request to insert or upload a file.
    It is used to perform the actual upload of the file.
    
    '''

    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading file...")
            _, response = insert_request.next_chunk()
            if response is not None:
                if "id" in response:
                    print(f"Video id '{response['id']}' was successfully uploaded.")
                else:
                    exit(f"The upload failed with an unexpected response: {response}")
        except HttpError as err:
            if err.resp.status in RETRIABLE_STATUS_CODES:
                error = (
                    f"A retriable HTTP error {err.resp.status} occurred:\n{err.content}"
                )
            else:
                raise
        except RETRIABLE_EXCEPTIONS as err:
            error = f"A retriable error occurred: {err}"

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                sys.exit("No longer attempting to retry.")

            max_sleep = 2**retry
            sleep_seconds = random.random() * max_sleep
            print(f"Sleeping {sleep_seconds} seconds and then retrying...")
            time.sleep(sleep_seconds)


def youtube_upload(video_metadata_path):
    '''The function `youtube_upload` uploads a video to YouTube using the video metadata provided in a JSON
    file.
    
    Parameters
    ----------
    video_metadata_path
        The `video_metadata_path` parameter is the path to a JSON file that contains the metadata for the
    video to be uploaded. This JSON file should include information such as the video file path, title,
    description, tags, and other relevant details.
    
    '''

    with open(video_metadata_path, "r", encoding="utf-8") as f:
        video_args = json.load(f)

    if not os.path.exists(video_args["video_file"]):
        exit("Please specify a valid file in the JSON.")

    youtube = get_authenticated_service()
    try:
        initialize_upload(youtube, video_args)
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
