from tweet_processor import TweetProcessor
from determine_relevance import RelevanceDeterminer
from news_articles_retriever import NewsArticlesRetriever, pretty_print_news

tp = TweetProcessor()
RelevanceDeterminer = RelevanceDeterminer(0)  # TODO: fix threshold
news_articles_retriever = NewsArticlesRetriever()

tweet, tweet_keywords = tp.extract_keywords(956956487225667584)
# print(tp.extract_keywords(956938973326098432))
# print(tp.extract_keywords(956937916374138880))

news_articles = news_articles_retriever.get_articles(tweet_keywords)

relevant_articles = RelevanceDeterminer.get_relevant_news(tweet, news_articles)

pretty_print_news(relevant_articles)
