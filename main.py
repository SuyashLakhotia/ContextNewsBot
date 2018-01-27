from twitter_utils import TweetProcessor
from news_utils import NewsRetriever, pretty_print_news
from determine_relevance import get_relevant_news

tweet_processor = TweetProcessor()
news_retriever = NewsRetriever()

tweet, tweet_entities, tweet_salience = tweet_processor.extract_entities(957267527649783808)

news_articles = news_retriever.get_articles(tweet_entities)

relevant_articles = get_relevant_news(tweet, tweet_entities, tweet_salience, news_articles, 0)

pretty_print_news(relevant_articles)
