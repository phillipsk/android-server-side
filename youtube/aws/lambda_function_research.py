from datetime import datetime
from itertools import accumulate
from typing import Pattern, List
from operator import mul
import re
import youtube_dl
import logging
import boto3
from botocore.exceptions import ClientError
import googleapiclient
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# s3_client = boto3.client('s3')
s3 = boto3.resource('s3')
DEVELOPER_KEY = os.environ.get('API_KEY_YT')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def lambda_handler(event, context):
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.environ.get('API_KEY_YT')

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    ret_videos_same = dict()
    ret_videos_uid = dict()
    # get_videos_same_dates('youtube#searchListResponse_HgGw699CfQZXkuRzLOJrPh2peRw_10_091020231527.json',
    #                       ret_videos_same, ret_videos_uid)
    get_videos_same_dates(get_yt_request(1, youtube, 'search', ret_videos_same),
                          ret_videos_same, ret_videos_uid)
    # get_yt_request(args, youtube, 'videos', ret_videos_same)

    # get_merge_videos('youtube#videoListResponse_DMl7bQ0vVf5VaH7gWDQ1-HIV2xE_4_091120181009.json',
    #              ret_videos_uid)
    get_merge_videos(get_yt_request(1, youtube, 'videos', ret_videos_same),
                     ret_videos_uid)

    download_mp3(ret_videos_uid)
    print('done')


def download_mp3(dict_videos_list):
    for k in dict_videos_list.keys():
        k = 'https://youtu.be/' + k
        # log.info(k)
        download(url=k, codec='mp3', bitrate=192)


def download(url: str, codec: str, bitrate: int, title: str = None, quiet: bool = True, force: bool = False):
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

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if title is None:
            title = info['title']
            try:
                print("Downloading...")
                # status = ydl.download([url])
            except:
                status = -1
            if info.get('title', None) != title:
                pass
            else:
                # fname = info.get('title', None) + '.mp3'
                fname = '8_9_2020 Worship Service.mp3'
                upload_file(fname, 'mcc-audio-lake')
                # s3.Object('mcc-audio-lake', fname).put(Body=open('/tmp/hello.txt', 'rb'))


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


def youtube_search(args, youtube):
    search_response = youtube.search().list(
        part="snippet",
        channelId="UC0clY7VjxRyRsfC6YWDlY6Q",
        maxResults=5,
        order="date",
        # videoDuration="long",
        q=args.q,
        type="video"
    ).execute()

    # nPmdkKu8VPs, 902ptouzJ-s, k1DnRR4U9b8, yBdx4Hi1hOg, 7JeaR6xlu6M
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            add_dict(search_result['snippet']['title'],
                     search_result['id']['videoId'])
            # object = YTresponse(search_result['id']['kind'],
            #                     search_result['id']['videoId'],
            #                     search_result['snippet']['publishedAt'],
            #                     search_result['snippet']['description'],
            #                     search_result['snippet']['title'])

            # url = 'https://youtu.be/' + search_result['id']['videoId']
            # title = search_result['snippet']['title']
            # date = search_result['snippet']['publishedAt']

            # if object.title in vids:
            #     v1 = vids[object.title]
            #
            #     vids[object.title] = object.getURL()
            # else:
            #     vids[object.title] = object.getURL()


class YouTubeVideo:
    def __init__(self, kind, videoId, publishedAt, description, title, channelId):
        self.kind = kind
        self.videoId = videoId
        self.publishedAt = publishedAt
        self.description = description
        self.title = title
        self.channelId = channelId

    def getURL(self):
        return 'https://youtu.be/' + self.videoId

    def getPublishedAt(self):
        return self.publishedAt


# p1 = YTresponse("John", 36)
# p1.myfunc()


def get_yt_request(count, youtube, api_reference='search', dict_videoIds=None):
    if api_reference.lower() == 'search':
        request = youtube.search().list(
            part="snippet",
            channelId="UC0clY7VjxRyRsfC6YWDlY6Q",
            maxResults=4,
            order="date",
            q="worship",
            videoDuration="long",
            type="video"
        ).execute()
    elif api_reference.lower() == 'videos' and bool(dict_videoIds):
        list_videoIds = list(dict_videoIds.keys())
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=list_videoIds,
            maxResults=10
        ).execute()
    else:
        return None

    response = request
    # filename = response['kind'] + "_" + response['etag'] + "_" + \
    #            str(response['pageInfo']['resultsPerPage'])
    # return file_write_json(response, filename, 'json')
    return response


def get_videos_same_dates(response, ret_videos_same: dict, ret_videos_uid: dict):
    f = response
    d = f.get('items', [])
    for k in d:
        p = get_date_iso(k['snippet']['publishedAt'])
        v = k['id']['videoId']
        for kk in d:
            pp = get_date_iso(kk['snippet']['publishedAt'])
            vv = kk['id']['videoId']
            if p == pp and v != vv:
                add_dict(v, k, ret_videos_same)
            # elif v not in ret_videos_uid and v not in ret_videos_same:
            #     add_dict(v, k, ret_videos_uid)
            #     log.debug(v)

    for k in d:
        p = get_date_iso(k['snippet']['publishedAt'])
        v = k['id']['videoId']
        if v not in ret_videos_same:
            add_dict(v, k, ret_videos_uid)


def get_merge_videos(response: object, ret_merge_dict: dict):
    if response is not None:
        f = response
        d = f.get('items', [])
        for k in d:
            # z = parse_udration(k['contentDetails']['duration'])
            t = extract_total_seconds_from_ISO8601(k['contentDetails']['duration'])
            p = get_date_iso(k['snippet']['publishedAt'])
            v = k['id']
            for kk in d:
                # zz = parse_udration(k['contentDetails']['duration'])
                tt = extract_total_seconds_from_ISO8601(kk['contentDetails']['duration'])
                pp = get_date_iso(kk['snippet']['publishedAt'])
                vv = kk['id']
                if p == pp and v != vv:
                    if t > tt:
                        add_dict(v, k, ret_merge_dict)
                    # else:
                    #     add_dict(v, k, ret_merge_dict)


def add_dict(key, val, return_dict):
    if key not in return_dict:
        # log.debug('dict added %s %s' % (key, len(return_dict)))
        print('dict added %s %s' % (key, len(return_dict)))
        return_dict[key] = val
    else:
        print('dict !added %s' % key)
        # log.debug('dict !added %s' % key)
    return return_dict


def clean_videos(dict):
    for dt in dict:
        vv = dict[dt]
        vvd = vv.getPublishedAt()
        for d in dict:
            d = YouTubeVideo.getPublishedAt()
            if dt == d:
                pass


def get_date_iso(str_date):
    return datetime.fromisoformat(str_date.replace("Z", "+00:00")).date()


SECONDS_PER_SECOND = 1
SECONDS_PER_MINUTE: int = 60
MINUTES_PER_HOUR: int = 60
HOURS_PER_DAY: int = 24
DAYS_PER_WEEK: int = 7
WEEKS_PER_YEAR: int = 52

ISO8601_PATTERN = re.compile(
    r"P(?:(\d+)Y)?(?:(\d+)W)?(?:(\d+)D)?"
    r"T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?"
)


def extract_total_seconds_from_ISO8601(iso8601_duration: str) -> int:
    """Compute duration in seconds from a Youtube ISO8601 duration format. """
    MULTIPLIERS: List[int] = (
        SECONDS_PER_SECOND, SECONDS_PER_MINUTE, MINUTES_PER_HOUR,
        HOURS_PER_DAY, DAYS_PER_WEEK, WEEKS_PER_YEAR
    )
    groups: List[int] = [int(g) if g is not None else 0 for g in
                         ISO8601_PATTERN.match(iso8601_duration).groups()]

    return sum(g * multiplier for g, multiplier in
               zip(reversed(groups), accumulate(MULTIPLIERS, mul)))


if __name__ == '__main__':
    lambda_handler(None, None)
