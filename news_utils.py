from newsapi import NewsApiClient


class NewsRetriever:

    def __init__(self):
        self.newsapiClient = NewsApiClient(api_key='0ff1cf9e1766451c8ed9c5825d57df45')
        self.list_of_sources = 'google-news,bbc-news,fox-news,cnn,the-new-york-times'
        self.articles = []

    def get_articles(self, phrases=''):
        response = self.newsapiClient.get_everything(q=phrases,
                                                     sources=self.list_of_sources,
                                                     language='en',
                                                     sort_by='relevancy',
                                                     page_size=10)
        status = response['status']
        if status != 'ok':
            print('Retrieved!')
        self.articles = response['articles']
        return self.articles


def pretty_print_news(articles=[]):
    for i in range(len(articles)):
        item = articles[i]
        print('\n---\n' + str(i) + '. ' + str(item['relevance_score']) + ' - ' +
              str(item['source']['name']) + ' - ' + item['title'] + ' - ' + item['description'] + '\n---\n')
