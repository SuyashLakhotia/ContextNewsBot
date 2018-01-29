from twitter_utils import TweetProcessor
from news_utils import NewsRetriever, pretty_print_news
from determine_relevance import get_relevant_news
from google_language import GoogleLanguage


def process_tweet(tweetID):
    tweet_processor = TweetProcessor()
    news_retriever = NewsRetriever()

    tweet = tweet_processor.get_tweet(tweetID)
    tweet_entities = tweet_processor.extract_entities(tweet)
    tweet_sentiment_score = get_tweet_sentiment(tweet["full_text"])

    if len(tweet_entities) == 0:
        return {"relevant_articles": [], "tweet_sentiment_score": tweet_sentiment_score, "wiki_urls": []}

    if tweet["user"]["verified"]:
        user_name = tweet["user"]["name"]
    else:
        user_name = None

    if tweet["place"] is not None:
        country = tweet["place"]["country"]
    else:
        country = None

    news_articles = news_retriever.get_articles(tweet_entities, country, user_name)
    relevant_articles = get_relevant_news(tweet, tweet_entities, news_articles, 0)

    wiki_urls = get_wiki_links(tweet_entities)

    response = {"relevant_articles": relevant_articles,
                "tweet_sentiment_score": tweet_sentiment_score,
                "wiki_urls": wiki_urls}

    return response


def get_tweet_sentiment(tweet):
    google_lang = GoogleLanguage()
    tweet_sentiment_score = google_lang.get_document_sentiment(tweet).score
    return tweet_sentiment_score


def get_wiki_links(tweet_entities):
    wikipedia_urls = []
    for entity in tweet_entities:
        if entity.salience > 0.5 and "wikipedia_url" in entity.metadata.keys():
            wikipedia_urls.append({"entity_name": entity.name, "wiki_url": entity.metadata["wikipedia_url"]})
            break

    return wikipedia_urls
