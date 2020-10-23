import json
import urllib.request


# url = curl -i -X GET \\

def get_data():
    url = "https://graph.facebook.com/v7.0/120085814675079/published_posts?limit=16&access_token=EAAEamWgsjN4BALOWf596hc8UKizZCzjv0zWE5wxzxUQLeAhCg5ZBAp89dT2OyRjB3miAskKfthA2pkFZCpltIQOjnud5Mf6t0kbySQQ5LYZCWFtGERPYU4TRsxdkn8CAOZBMRc3SZCJjHRBu2yvVjVS4Yh1QcUAyS35kQddu6e3jUaVC6wRuENg7UAw1xEykb81D2Yxk8edgZDZD"
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    data = response.read()
    values = json.loads(data)
    return values


if __name__ == '__main__':
    ss = get_data()
    print("done")
