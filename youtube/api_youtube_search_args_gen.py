#!/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import argparse

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


def youtube_search(options):
    # youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    #                 developerKey=DEVELOPER_KEY)
    youtube = googleapiclient.discovery.build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        part='snippet',
        maxResults=options.max_results,
        publishedAfter="2020-01-01T00:00:00Z",
        q=options.q,
        regionCode="US",
        relevanceLanguage="en",
        type="video"
    ).execute()

    c = search_response['pageInfo']['totalResults']
    print("Total results for keyword == " + args.q + " == " + str(c))
    # videos = []
    channels = []
    playlists = []
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    # for search_result in search_response.get('items', []):
    #     if search_result['id']['kind'] == 'youtube#video':
    #         videos.append('%s (%s)' % (search_result['snippet']['title'],
    #                                    search_result['id']['videoId']))
    # elif search_result['id']['kind'] == 'youtube#channel':
    #   channels.append('%s (%s)' % (search_result['snippet']['title'],
    #                                search_result['id']['channelId']))
    # elif search_result['id']['kind'] == 'youtube#playlist':
    #   playlists.append('%s (%s)' % (search_result['snippet']['title'],
    #                                 search_result['id']['playlistId']))

    # print(len(search_response.get('items', [])))
    # print('Videos:\n', '\n'.join(videos), '\n')
    # print('Channels:\n', '\n'.join(channels), '\n')
    # print('Playlists:\n', '\n'.join(playlists), '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default='zuul, netflix')
    parser.add_argument('--type', help='Search term', default='video')
    parser.add_argument('--max-results', help='Max results')
    args = parser.parse_args()

    try:
        youtube_search(args)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
