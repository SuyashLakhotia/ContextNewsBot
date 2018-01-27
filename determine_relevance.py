import paralleldots


class RelevanceDeterminer:
    def __init__(self, threshold=3.5):
        self.threshold = threshold

        paralleldots.set_api_key("siQChQ9PVPRs8Gm0HDawsqscverucbEq77zNBZpNXI8")

    def get_relevant_news(self, tweet, news_set):
        """
        Args:
            tweet (str): Incoming tweet
            news_set (List): List of news items

        Returns:
            relevant_news_set (List): Filtered list of relevant news items.
        """
        relevant_news_set = []
        for item in news_set:
            if self._relevance_score(tweet, item) >= self.threshold:
                relevant_news_set.append(item)
        return relevant_news_set

    def _relevance_score(self, tweet, news_item):
        # TODO depends on structure of news_item and API response
        api_response = paralleldots.similarity(tweet, news_item)
        return api_response['normalized_score']


if __name__ == '__main__':
    RelevanceDeterminer = RelevanceDeterminer(3.5)
    
    tweet = "Donald Trump is correct about global warming. Total farce."
    news_set = [
                "Prime Minister Modi gives very good speeches.", 
                "Global warming is scientifically true. Researchers have found evidence.", 
                "Donald Trump lies about facts nine out of ten times."
                ]

    print(RelevanceDeterminer.get_relevant_news(tweet, news_set))
