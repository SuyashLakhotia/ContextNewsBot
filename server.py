# TODO: Make this compatible with everything else (especially new code structrue)

from flask import Flask, jsonify, redirect, request
from flask_restful import Api, Resource

from tweet_processor import TweetProcessor
from determine_relevance import RelevanceDeterminer
from news_articles_retriever import NewsArticlesRetriever, pretty_print_news

app = Flask(__name__)
APP_URL = "http://127.0.0.1:5000"

tp = TweetProcessor()
RelevanceDeterminer = RelevanceDeterminer(0)
news_articles_retriever = NewsArticlesRetriever()


class Tweets(Resource):

    def post(self):
        data = request.get_json()
        if not data:
            data = {"response": "ERROR"}
            return jsonify(data)
        else:
            id = data.get("id")
            tweet, tweet_keywords = tp.extract_keywords(int(id))
            news_articles = news_articles_retriever.get_articles(tweet_keywords)
            return RelevanceDeterminer.get_relevant_news(tweet, news_articles)

api = Api(app)
api.add_resource(Tweets, "/tweet", endpoint="tweet")


if __name__ == "__main__":
    app.run(debug=True)
