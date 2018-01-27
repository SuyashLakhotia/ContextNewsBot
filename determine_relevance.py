import paralleldots

from news_articles_retriever import NewsArticlesRetriever, pretty_print_news

class RelevanceDeterminer:
    def __init__(self, threshold=3.5):
        self.threshold = threshold

        paralleldots.set_api_key("siQChQ9PVPRs8Gm0HDawsqscverucbEq77zNBZpNXI8")

    def get_relevant_news(self, tweet, news_articles):
        """
        Args:
            tweet (str): Incoming tweet
            news_articles (List): Response of News Retriever

        Returns:
            relevant_news_articles (List): Filtered list of relevant news items.
        """
        relevant_news_articles = []
        for item in news_articles:
            if self._relevance_score(tweet, item['title']+ " " + item['description']) >= self.threshold:
                relevant_news_articles.append(item)
        return relevant_news_articles

    def _relevance_score(self, tweet, news_item):
        # TODO depends on structure of news_item and API response
        api_response = paralleldots.similarity(tweet, news_item)
        return api_response['normalized_score']


if __name__ == '__main__':
    RelevanceDeterminer = RelevanceDeterminer(0)

    tweet = "All terrorists are Muslim"

    news_articles_retriever = NewsArticlesRetriever()
    news_articles = news_articles_retriever.get_articles(tweet)
    # news_set = [
    #             "Prime Minister Modi gives very good speeches.", 
    #             "Global warming is scientifically true. Researchers have found evidence.", 
    #             "Donald Trump lies about facts nine out of ten times."
    #             ]

    relevant_articles = RelevanceDeterminer.get_relevant_news(tweet, news_articles)
    
    pretty_print_news(relevant_articles)