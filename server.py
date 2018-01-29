import os
import credentials

# needs to be before `import process_tweet`
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials.PATH_TO_GOOGLE_JSON

from flask import Flask, jsonify, redirect, request
from flask_restful import Api, Resource

from process_tweet import process_tweet


app = Flask(__name__)
APP_URL = "http://127.0.0.1:5000"


class Tweets(Resource):

    def post(self):
        data = request.get_json()
        if not data:
            data = {"response": "ERROR"}
            return jsonify(data)
        else:
            tweetID = data.get("id")
            data = process_tweet(tweetID)
            return jsonify(data)

api = Api(app)
api.add_resource(Tweets, "/tweet", endpoint="tweet")


if __name__ == "__main__":
    app.run(debug=True)
