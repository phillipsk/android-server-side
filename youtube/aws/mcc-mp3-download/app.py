from chalice import Chalice, Rate, Response
import os
import youtube_dl
import logging
import boto3
from botocore.exceptions import ClientError
import googleapiclient
from googleapiclient.discovery import build

YOUTUBE_DEVELOPER_KEY = os.environ.get('API_KEY_YT')

S3_BUCKET = 'mcc-audio-lake'  # bucket name
s3_client = boto3.resource('s3')

app = Chalice(app_name='mcc-mp3-download')


@app.route('/')
def index():
    return {'hello': 'world'}


#
# # Automatically runs every 5 minutes
# @app.schedule(Rate(5, unit=Rate.MINUTES))
# def periodic_task(event):
#     # lambda_handler(None, None)
#     return {"hello": "world"}

# curl -X PUT https://g2csjrn5q3.execute-api.us-east-1.amazonaws.com/api/test.mp3 --upload-file mypic.jpg --header "Content-Type:application/octet-stream"
@app.route('/upload/{file_name}', methods=['PUT'],
           content_types=['application/octet-stream'])
def upload_to_s3(file_name):
    # get raw body of PUT request
    body = app.current_request.raw_body

    # write body to tmp file
    tmp_file_name = '/tmp/' + file_name
    with open(tmp_file_name, 'wb') as tmp_file:
        tmp_file.write(body)

    # upload tmp file to s3 bucket
    s3_client.upload_file(tmp_file_name, S3_BUCKET, file_name)

    return Response(body='upload successful: {}'.format(file_name),
                    status_code=200,
                    headers={'Content-Type': 'text/plain'})


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

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
        ydl.download([url])
        os.rename(info.get('title', None) + '.' + codec,
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
