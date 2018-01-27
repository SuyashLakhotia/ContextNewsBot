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
        if key == "tfidf":
            return self.tfidf(tweet, news_articles, threshold=0) 
            # TODO set threshold
        elif key == "cosine_similarity":
            return self.cosine_similarity(tweet, news_articles, threshold=0)
            # TODO set threshold
        else:
            relevant_news_articles = []
            for item in news_articles:
                relevance_score = self._relevance_score(tweet, item['title']+ ". " + item['description'])
                if relevance_score >= self.threshold:
                    item["relevance_score"] = relevance_score
                    relevant_news_articles.append(item)
            return relevant_news_articles

    def _relevance_score(self, tweet, news_item, key="dandelion"):
        """Similarity API based scoring metrics
        """
        # TODO: depends on structure of news_item and API response
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

            # TODO: decision tree kind of model? But API calls are expensive!
            if syntactic_score >= 0.5:
                # TODO: figure out syntactic similarity threshold
                return semantic_score
            else:
                return -1

    def tfidf(self, tweet, news_articles, threshold=0.5):
        # TODO tfidf can also be calculated in batches
        import gensim
        from nltk.tokenize import word_tokenize

        news_articles_text = [item['title']+ ". " + item['description'] for item in news_articles]
        news_articles_tokenized = [[w.lower() for w in word_tokenize(item)] 
            for item in news_articles_text]
        
        dictionary = gensim.corpora.Dictionary(news_articles_tokenized)
        corpus = [dictionary.doc2bow(item_tokenized) for item_tokenized in news_articles_tokenized]
        tf_idf = gensim.models.TfidfModel(corpus)
        sims = gensim.similarities.Similarity('',tf_idf[corpus],
                                      num_features=len(dictionary))

        tweet_tokenized = [w.lower() for w in word_tokenize(tweet)]
        tweet_tokenized_bow = dictionary.doc2bow(tweet_tokenized)
        tweet_tokenized_tf_idf = tf_idf[tweet_tokenized_bow]
        
        relevant_news_articles = []
        for idx, similarity_score in enumerate(sims[tweet_tokenized_tf_idf]):
            if similarity_score >= threshold:
                news_articles[idx]["relevance_score"] = similarity_score
                relevant_news_articles.append(news_articles[idx])

        return relevant_news_articles

    def cosine_similarity(self, tweet, news_articles, threshold=0.5):
        # TODO download spacy models
        import spacy
        nlp = spacy.load('en_core_web_sm')
        news_articles_vectors = [nlp(item['title']+ ". " + item['description']) for item in news_articles]
        tweet_vector = nlp(tweet)

        relevant_news_articles = []
        for idx, item in enumerate(news_articles_vectors):
            similarity_score = tweet_vector.similarity(item)
            if similarity_score >= threshold:
                news_articles[idx]["relevance_score"] = similarity_score
                relevant_news_articles.append(news_articles[idx])

        return relevant_news_articles


if __name__ == '__main__':
    RelevanceDeterminer = RelevanceDeterminer(0)

    tweet = "Donald Trump global warming"

    news_articles_retriever = NewsArticlesRetriever()
    
    news_articles = news_articles_retriever.get_articles(tweet.split(' '))
    print(len(news_articles))
    t = time.time()
    relevant_articles = RelevanceDeterminer.get_relevant_news(tweet, news_articles, 'cosine_similarity')
    print(time.time()-t)
    pretty_print_news(relevant_articles)
