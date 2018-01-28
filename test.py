from twitter_utils import TweetProcessor
from news_utils import NewsRetriever, pretty_print_news
from determine_relevance import get_relevant_news

tweet_processor = TweetProcessor()
news_retriever = NewsRetriever()

tweet = tweet_processor.get_tweet(957220637705109505)
tweet_entities = tweet_processor.extract_entities(tweet)

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

pretty_print_news(relevant_articles)
