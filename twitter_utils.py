import requests
import base64
import html
import re

import credentials
from google_language import GoogleLanguage


class TweetProcessor(object):

    def __init__(self):
        self.base_url = 'https://api.twitter.com/'

        access_token = self._authorize_twitter()
        self.query_headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }

        self.google_lang = GoogleLanguage()

    def _authorize_twitter(self):
        key_secret = '{}:{}'.format(credentials.TWITTER_API_KEY,
                                    credentials.TWITTER_API_SECRET).encode('ascii')
        b64_encoded_key = base64.b64encode(key_secret).decode('ascii')

        auth_url = '{}oauth2/token'.format(self.base_url)
        auth_headers = {
            'Authorization': 'Basic {}'.format(b64_encoded_key),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        auth_data = {
            'grant_type': 'client_credentials'
        }
        auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
        assert auth_resp.status_code == 200
        return auth_resp.json()['access_token']

    def extract_entities(self, tweet):
        text = tweet['full_text']
        text = html.unescape(text)  # unescape html text
        text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', text)  # remove links
        re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+',
               '', text)  # remove emoji

        names = []
        salience = []
        print('Text: {}'.format(text))

        if False:
            sentiment = self.google_lang.get_sentiment(text)
            print('Sentiment: {}, {}'.format(sentiment.score,
                                             sentiment.magnitude))

        if False:
            entities = self.google_lang.get_entities_sentiment(text)
            for entity in entities:
                print('Entity: {}'.format(entity.name))
                print('Sentiment: {}'.format(entity.sentiment.score, entity.sentiment.magnitude))

        entities = self.google_lang.get_entities(text)
        for entity in entities:
            print('Entity: {}'.format(entity.name))
            print('Salience: {}'.format(entity.salience))
            names.append(entity.name)
            salience.append(entity.salience)

        return entities, names, salience

    def get_tweet(self, tweet_id):
        query_params = {
            'id': tweet_id,
            'tweet_mode': 'extended'
        }
        search_url = '{}1.1/statuses/show.json'.format(self.base_url)
        search_resp = requests.get(search_url, headers=self.query_headers, params=query_params)
        tweet_data = search_resp.json()
        return tweet_data
