import os, json
from fb.facebook import GraphAPI
import requests


def conn_fb():
    """
    A simple example script to get all posts on a user's timeline.
    Originally created by Mitchell Stewart.
    <https://gist.github.com/mylsb/10294040>
    """

    def some_action(post):
        """ Here you might want to do something with each post. E.g. grab the
        post's message (post['message']) or the post's picture (post['picture']).
        In this implementation we just print the post's created time.
        """
        print(post["full_picture"])

    # You'll need an access token here to do anything.  You can get a temporary one
    # here: https://developers.facebook.com/tools/explorer/
    access_token = access_token = os.environ.get('API_KEY_FB')
    # Look at Bill Gates's profile for this example by using his Facebook id.
    user = CLIENT_SECRET = os.environ.get('API_USER_FB')

    graph = GraphAPI(access_token)
    profile = graph.get_object(user)
    d1 = {'icon': 'icon', 'full_picture': 'full_picture'}
    posts = graph.get_connections(profile["id"], 'published_posts', args=d1)
    # posts = graph.get_connections(profile["id"], "posts", 'picture', 'full_picture',
    #                               'attachments', 'icon',)

    # Wrap this block in a while loop so we can keep paginating requests until
    # finished.
    while True:
        try:
            # Perform some action on each post in the collection we receive from
            # Facebook.
            # [some_action(post=post) for post in posts["data"]]
            for post in posts['data']:
                event = graph.get_object(id=post['id'],
                                         fields='full_picture,icon,message,created_time')
                some_action(event)
            # Attempt to make a request to the next page of data, if it exists.
            posts = requests.get(posts["paging"]["next"]).json()
        except KeyError:
            # When there are no more pages (['paging']['next']), break from the
            # loop and end the script.
            break


def read_json():
    filename = "api_graph_fb_curl_V.json"
    with open(filename) as f:
        data = json.loads(f.read())
        print(data[0]['text'])


# return data.get('results').get('transcripts')[0].get('transcript')


if __name__ == '__main__':
    # graph = GraphAPI(access_token="EAAEamWgsjN4BAP3ozf8kErbPYt2cEu6RTsHPJbtgvkwhVOYzV525kZCwmHjezmiZBRIZAwkiG1ImOxShyhsrrudkPHjIugaFtTTSU6pPNvbbX1dBFXWQhu0ma9k1q318aZAeLx4cq9jvcyx5KvgCsPIY9tzUKZBQS1AsLcZB5ZCZBQ111ISpLABz",
    #                  version="4.0")
    # read_json()
    conn_fb()
    print('done')
