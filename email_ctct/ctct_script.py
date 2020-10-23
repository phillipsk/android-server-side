import base64
import json
import os

import requests


def base64_encode_string(s):
    return base64.b64encode(s.encode()).decode()

def file_write_json(data, filename, ext=None):
    #   TODO: changes 10/9/20 ensure compatibility with YouTube impl
    if ext:
        filename = filename + "_" + set_timestamp() + "." + ext
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return filename


def file_read_json(filename):
    # while not os.path.exists(filename):
    #     pass  # time.sleep(1)
    if os.path.isfile(filename):
        with open(filename) as f:
            return json.load(f)
    else:
        raise ValueError("%s isn't a file!" % filename)


class MyAPI:
    def __init__(self, token_url, client_id, client_secret):
        self.token_url = token_url
        self.token = None
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = None

    def get_token(self, auth=False, code=""):
        headers = {
            'Authorization': 'Basic ' +
                             base64_encode_string(self.client_id + ':' + self.client_secret),
            # 'Content-Type': 'application/x-www-form-urlencoded',
        }

        if auth:
            params = {'code': code,
                      'grant_type': 'authorization_code'}
        else:
            params = {'refresh_token': code,
                      'grant_type': 'refresh_token'}

        r = requests.post(self.token_url, headers=headers, params=params)

        self.token = r.json()['access_token']
        self.refresh_token = r.json()['refresh_token']
        file_write_json(r.json(), FILENAME)
        return self.token

    def endpoint(self, url):
        if self.token is None:
            self.get_token()

        headers = {'Authorization': 'Bearer ' + self.token}

        r = requests.get(url, headers=headers)

        if r.status_code == 401:
            # status code timed out, refresh token
            self.token = None
            return self.endpoint(url)

        return r.json()


if __name__ == '__main__':
    CLIENT_ID = os.environ.get('API_KEY_CC')
    CLIENT_SECRET = os.environ.get('API_KEY_CC_SECRET')
    FILENAME = 'cc_response.json'
    # AUTH_CODE = 'GKz0m-FEMulV47_LXMX1-IoKHZ_xg1dOG1rl3gEt'
    ###
    ###
    f = file_read_json(FILENAME)
    rt = f['refresh_token']
    ctAPI = MyAPI('https://idfed.constantcontact.com/as/token.oauth2',
                  CLIENT_ID, CLIENT_SECRET)
    ctAPI.refresh_token = rt

    print('Before = ' + ctAPI.refresh_token)
    refresh_token = ctAPI.get_token(auth=False, code=ctAPI.refresh_token)
    print('After = ' + ctAPI.refresh_token)

