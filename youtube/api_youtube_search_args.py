#!/usr/bin/python
# -*- coding: utf-8 -*-

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..
import logging
from datetime import datetime

import argparse
from youtube import audiosave_class
from reusable.maintenance import *

import googleapiclient
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

DEVELOPER_KEY = os.environ.get('API_KEY_YT')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'



# def init():
# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.

# youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
#                 developerKey=DEVELOPER_KEY)

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


def get_download_mp3(dict_videos_list):
    for k in dict_videos_list.keys():
        k = 'https://youtu.be/' + k
        log.info(k)
        audiosave_class.download(url=k, codec='mp3',
                                 bitrate=192)


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


def get_yt_request(args, youtube, api_reference='search', dict_videoIds=None):
    if api_reference.lower() == 'search':
        request = youtube.search().list(
            part="snippet",
            channelId="UC0clY7VjxRyRsfC6YWDlY6Q",
            maxResults=args.max_results,
            order="date",
            q=args.q,
            videoDuration="long",
            type="video"
        ).execute()
    elif api_reference.lower() == 'videos' and dict_videoIds is not None:
        list_videoIds = list(dict_videoIds.keys())
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=list_videoIds,
            maxResults=args.max_results
        ).execute()
    else:
        exit()

    response = request
    filename = response['kind'] + "_" + response['etag'] + "_" + \
               str(response['pageInfo']['resultsPerPage'])
    return file_write_json(response, filename, 'json')


def get_videos_same_dates(filename, ret_videos_same: dict, ret_videos_uid: dict):
    f = file_read_json(filename)
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


def get_merge_videos(filename: object, ret_merge_dict: dict):
    f = file_read_json(filename)
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
        log.debug('dict added %s %s' % (key, len(return_dict)))
        return_dict[key] = val
    else:
        log.debug('dict !added %s' % key)
    return return_dict

    # if p not in ret_videos_same:
    #     if p not in ret_videos_same:
    #     log.info(f'error {key} {val} ')
    #     ret_videos_same[key] = val
    # else:
    #     log.info(f'added {key} {val} ')

    # pass

    # exit()

    # videos = []
    # context = {}
    # for video in videos_results:
    #     video_content = {
    #         'title': video['snippet']['title'],
    #         'id': video['id'],
    #         # 'duration': parse_duration(video['contentDetails']['duration']),
    #         'thumbnail': video['snippet']['thumbnails']['high']['url']
    #     }
    #     videos.append(video_content)
    #
    # context = {
    #     'videos': videos
    # }
    # holder = {}
    # holder = {r: YouTubeVideo(kind=r['id']['kind'],
    #                              videoId=r['id']['videoId'],
    #                              description=r['snippet']['description'],
    #                              publishedAt=r['snippet']['publishedAt'],
    #                              title=r['snippet']['title'],
    #                              channelId=r['snippet']['channelId'])
    #           for r in response.get('items', [])}

    # for r in f.get('items', []):
    #     if r['id']['kind'] == 'youtube#video':
    #         YouTubeVideo(kind=r['id']['kind'],
    #                      videoId=r['id']['videoId'],
    #                      description=r['snippet']['description'],
    #                      publishedAt=r['snippet']['publishedAt'],
    #                      title=r['snippet']['title'],
    #                      channelId=r['snippet']['channelId'])
    #
    #     add_dict(r['id']['videoId'], YouTubeVideo)


def clean_videos(dict):
    for dt in dict:
        vv = dict[dt]
        vvd = vv.getPublishedAt()
        for d in dict:
            d = YouTubeVideo.getPublishedAt()
            if dt == d:
                pass


if __name__ == '__main__':
    # TODO: script will execute daily
    #   query options should only be max 1
    #   or check for existing videos
    # cron job
    #  TODO: handle duplicate videos
    #     sort by upload date
    #  TODO: handle abbreviated videos
    #      concatenate?

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.environ.get('API_KEY_YT')

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    logging.basicConfig(level=logging.DEBUG)
    hdlr = logging.FileHandler('py_debug_requests.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)

    log = logging.getLogger(__name__)
    log.addHandler(hdlr)
    # log.setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default='worship')
    parser.add_argument('--max-results', help='Max results', default=10)
    args = parser.parse_args()

    try:
        # youtube_search(args)
        # request_yt_get_search(args, youtube)
        # get_videos_same_dates(request_yt_get_search(args, youtube))
        ret_videos_same = dict()
        ret_videos_uid = dict()
        # get_videos_same_dates('youtube#searchListResponse_HgGw699CfQZXkuRzLOJrPh2peRw_10_091020231527.json',
        #                       ret_videos_same, ret_videos_uid)
        get_videos_same_dates(get_yt_request(args, youtube, 'search', ret_videos_same),
                              ret_videos_same, ret_videos_uid)
        # get_yt_request(args, youtube, 'videos', ret_videos_same)

        # get_merge_videos('youtube#videoListResponse_DMl7bQ0vVf5VaH7gWDQ1-HIV2xE_4_091120181009.json',
        #              ret_videos_uid)
        get_merge_videos(get_yt_request(args, youtube, 'videos', ret_videos_same),
                         ret_videos_uid)

        get_download_mp3(ret_videos_uid)
        # clean_videos(vids)
        log.info("done")
    except HttpError as e:
        log.info('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

    # sub_proc_dl(vids)

# 'youtube#searchListResponse_Tcc_j_nc5u5uiuC5cPYWQ3dEFmU_10'
