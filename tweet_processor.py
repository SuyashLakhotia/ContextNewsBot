import requests
import base64

from google.cloud import language
from google.cloud.language import types

import credentials


class TweetProcessor(object):

    def __init__(self):
        key_secret = '{}:{}'.format(credentials.TWITTER_API_KEY,
                                    credentials.TWITTER_API_SECRET).encode('ascii')
        b64_encoded_key = base64.b64encode(key_secret).decode('ascii')

        self.base_url = 'https://api.twitter.com/'

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

        access_token = auth_resp.json()['access_token']
        self.query_headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }

    def extract_keywords(self, tweet_id):
        text = self.get_text(tweet_id)
        keywords = []

        print('Text: {}'.format(text))
        document = types.Document(content=text,
                                  type='PLAIN_TEXT')

        client = language.LanguageServiceClient()

        if False:
            sentiment = client.analyze_sentiment(document=document,
                                                 encoding_type='UTF32').document_sentiment
            print('Sentiment: {}, {}'.format(sentiment.score,
                                             sentiment.magnitude))

        if False:
            response = client.analyze_entity_sentiment(document=document,
                                                       encoding_type='UTF32')
            for entity in response.entities:
                print('Entity: {}'.format(entity.name))
                print('Sentiment: {}'.format(entity.sentiment.score, entity.sentiment.magnitude))

        if True:
            response = client.analyze_entities(document=document,
                                               encoding_type='UTF32')
            for entity in response.entities:
                print('Entity: {}'.format(entity.name))
                keywords.append(entity.name)

        return keywords

    def get_text(self, tweet_id):
        query_params = {
            'id': tweet_id,
            'tweet_mode': 'extended'
        }
        search_url = '{}1.1/statuses/show.json'.format(self.base_url)
        search_resp = requests.get(search_url, headers=self.query_headers, params=query_params)
        tweet_data = search_resp.json()
        return tweet_data['full_text']
