import paralleldots
import requests

from news_articles_retriever import NewsArticlesRetriever, pretty_print_news

import time


class RelevanceDeterminer:
    def __init__(self, threshold=3.5):
        self.threshold = threshold

    def get_relevant_news(self, tweet, news_articles, key="dandelion"):
        """
        Args:
            tweet (str): Incoming tweet
            news_articles (List): Response of News Retriever
            key (str): Relevance metric/selector

        Returns:
            relevant_news_articles (List): Filtered list of relevant news items.
        """
        relevant_news_articles = []
        for item in news_articles:
            t = time.time()
            relevance_score = self._relevance_score(tweet, item['title']+ ". " + item['description'], key)
            print("relevence score-> ", time.time() - t)
            if relevance_score >= self.threshold:
                item["relevance_score"] = relevance_score
                relevant_news_articles.append(item)
        return relevant_news_articles

    def _relevance_score(self, tweet, news_item, key="dandelion"):
        # TODO depends on structure of news_item and API response
        
        if key == "paralleldots":
            # direct semantic similarity
            paralleldots.set_api_key("siQChQ9PVPRs8Gm0HDawsqscverucbEq77zNBZpNXI8")
            api_response = paralleldots.similarity(tweet, news_item)
            return api_response['normalized_score']

        elif key == "dandelion":
            # semantic + syntactic similarity score
            base_url = "https://api.dandelion.eu/datatxt/sim/v1/"
            text1 = tweet.replace(" ", "%20")
            text2 = news_item.replace(" ", "%20")
            api_key = "9e90047b495448adbab611edd14fae3e"

            url_semantic = base_url + '?text1=' + text1 + '&text2=' + text2 + '&bow=never' + "&token=" + api_key
            api_response_semantic = requests.post(url_semantic).json()

            url_syntactic = base_url + '?text1=' + text1 + '&text2=' + text2 + '&bow=always' + "&token=" + api_key
            api_response_syntactic = requests.post(url_semantic).json()

            semantic_score = api_response_semantic['similarity']
            syntactic_score = api_response_syntactic['similarity']

            # TODO decision tree kind of model? But API calls are expensive!
            if syntactic_score >= 0.5:
                # TODO figure out syntactic similarity threshold
                return semantic_score
            else:
                return -1


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
