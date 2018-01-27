from newsapi import NewsApiClient
from google_language import IMP_ENTITY_IDX


class NewsRetriever:

    def __init__(self):
        self.newsapiClient = NewsApiClient(api_key='0ff1cf9e1766451c8ed9c5825d57df45')
        self.list_of_sources = 'buzzfeed,bbc-news,fox-news,cnn,the-new-york-times'

    def get_articles(self, entities, country=None, user_name=None):
        phrases = []
        for entity in entities:
            if entity.type in IMP_ENTITY_IDX:
                phrases.append(entity.name)

        if country is not None:
            phrases.append(country)

        if user_name is not None:
            phrases.append(user_name)

        response = self.newsapiClient.get_everything(q=['+' + phrase for phrase in phrases],
                                                     sources=self.list_of_sources,
                                                     language='en',
                                                     sort_by='relevancy',
                                                     page_size=10)
        status = response['status']
        if status != 'ok':
            print('Retrieved!')

        return response['articles']


def pretty_print_news(articles):
    for i in range(len(articles)):
        item = articles[i]
        print('\n---\n' + str(i) + '. ' + str(item['relevance_score']) + ' - ' +
              str(item['source']['name']) + ' - ' + item['title'] + ' - ' + item['description'] + '\n---\n')
