from newsapi import NewsApiClient


class NewsArticlesRetriever:
    def __init__(self):
        self.newsapiClient = NewsApiClient(api_key='0ff1cf9e1766451c8ed9c5825d57df45')
        self.list_of_sources = 'bbc-news,cnn,google-news'
        self.articles = []

    def get_articles(self, phrases=''):
        response = self.newsapiClient.get_everything(q=phrases,
                                          sources=self.list_of_sources,
                                          domains='bbc.co.uk',
                                          from_parameter='2017-12-01',
                                          language='en',
                                          sort_by='relevancy')
        status = response['status']
        if status != 'ok':
            print('Retrived!')
        self.articles = response['articles']
        return self.articles


def pretty_print_news(articles=[]):
    for item in articles:
        print('\n---\n' + item['relevance_score'] + ' - ' + item['title'] + ' - ' + item['description'] + '\n---\n')


if __name__=='__main__':
    print(getArticles('Trump Global Warming'))