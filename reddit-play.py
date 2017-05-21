import requests
import requests.auth
from datetime import datetime, timedelta

from secrets import SECRET


USER_AGENT = 'PlayingWithReddit:v0.0 by /u/awarnes'


def check_time(request_time):
    """Helper function to ensure validity of access_token"""

    return request_time + timedelta(seconds=3600) > datetime.now()


def get_token(SECRET, USER_AGENT):
    """
    Retrieves an access token for the reddit api and marks the time that the request was sent.
    Returns a dictionary with response information and request time.
    """
    client_auth = requests.auth.HTTPBasicAuth(SECRET['client_id'], SECRET['client_secret'])
    post_data = {'grant_type': 'password', 'username': 'awarnes', 'password': SECRET['password']}
    headers = {'User-Agent': USER_AGENT}

    req_time = datetime.now()

    response = requests.post('https://www.reddit.com/api/v1/access_token',
                              auth=client_auth, data=post_data, headers=headers)

    resp_dict = response.json()

    resp_dict['req_time'] = req_time

    return resp_dict

def get_user(access_resp, USER_AGENT):
    """
    Uses access_token to get user information for the account.
    Returns a dictionary.
    """

    if check_time(access_resp['req_time']):
        headers = {'Authorization': 'bearer {}'.format(access_resp['access_token']), 'User-Agent': USER_AGENT}
        response = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
        return response.json()

    print('Access token expired!')

def post_to_reddit(access_resp, USER_AGENT, post):
    """
    Posts to a subreddit!

    post is  a dict w/ subreddit name, title, and text
    """

    if check_time(access_resp['req_time']):
        headers = {'Authorization': 'bearer {}'.format(access_resp['access_token']), 'User-Agent': USER_AGENT}
        post_data = {'api_type': 'json', 'kind': 'self', 'sr': post['sr'], 'text': post['text'], 'title': post['title']}
        response = requests.post('https://oauth.reddit.com/api/submit', data=post_data, headers=headers)

        return response.json()

    print('Access token expired!')

access_resp = get_token(SECRET, USER_AGENT)

post = {'sr': 'pythonforengineers', 'text': 'Snek is sweet!', 'title': 'I love Python!'}

print(post_to_reddit(access_resp, USER_AGENT, post))
