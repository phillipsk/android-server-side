# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import googleapiclient.discovery
import configparser
config = configparser.configparser()
config.read("config.ini")

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"


    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=config.get('apikeys','yt'))

    search_response = youtube.search().list(
        part="snippet",
        channelId="UC0clY7VjxRyRsfC6YWDlY6Q",
        maxResults=5,
        order="date",
        q="worship",
        type="video"
    ).execute()

    videos = []
    # vids = {}
    # people = ((data["name"], data["number"]) for data in json.loads(some_list)[::-1])
    # phoneBook = dict(people)

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            add_vid(search_result['id']['videoId'],
                    search_result['snippet']['title'])
            # videos.append('%s (%s)' % (search_result['snippet']['title'],
            #                            search_result['id']['videoId']))

    # print('Videos:\n', '\n'.join(videos), '\n')
    # youtube.com/embed{w1CGfNOBCG4}
    # https://www.youtube.com/watch?v=w1CGfNOBCG4
    # https://youtu.be/w1CGfNOBCG4
    # https://www.youtube.com/embed/w1CGfNOBCG4
    # print(response)


def add_vid(url, title):
    if url in vids:
        print(f'error {url} {title} ')
    else:
        vids[url] = title


if __name__ == "__main__":
    vids = dict()
    main()
    print("done")
