# lambda_function.py
import os
import youtube_dl
import logging
import boto3
from botocore.exceptions import ClientError
import googleapiclient
from googleapiclient.discovery import build

YOUTUBE_DEVELOPER_KEY = os.environ.get('API_KEY_YT')
s3 = boto3.resource('s3')


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download(url: str, codec: str, bitrate: int, title: str = None,
             quiet: bool = True, force: bool = False):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': codec,
            'preferredquality': str(bitrate),
        }],
        'outtmpl': '%(title)s.%(etx)s',
        'quiet': quiet
    }
    # TODO: this library actually accepts a list of urls []
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        ydl.cache.remove()
        ydl.download([url])
        os.rename(info.get('title', None).replace('/', '_') + '.' + codec,
                  title + '.' + codec)


def lambda_handler(event, context):
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=YOUTUBE_DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet", channelId="UC0clY7VjxRyRsfC6YWDlY6Q", maxResults=1,
        order="date", q="worship", videoDuration="long", type="video").execute()

    response = request.get('items', [])
    url = 'https://youtu.be/' + response[0]['id']['videoId']
    # debug
    url = 'https://youtu.be/WNugv3ut0sk'
    url = 'https://youtu.be/eTH0OVkuD3E'
    title = response[0]['snippet']['title']
    title = 'Worship sample'

    download(url=url, codec='mp3', bitrate=192, title=title, quiet=True)

    print('done')


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


if __name__ == '__main__':
    lambda_handler(None, None)
