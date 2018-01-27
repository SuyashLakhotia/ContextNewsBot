import requests

import paralleldots
from google_language import GoogleLanguage

from news_utils import pretty_print_news


def get_relevant_news(tweet, tweet_keywords, tweet_salience, news_articles, threshold):
    relevant_news_articles = []
    for item in news_articles:
        relevance_score = relevance_score_google(tweet, tweet_keywords, tweet_salience,
                                                 item['title'] + ". " + item['description'])
        if relevance_score >= threshold:
            item["relevance_score"] = relevance_score
            relevant_news_articles.append(item)
    return relevant_news_articles


def relevance_score_google(tweet, tweet_keywords, tweet_salience, news_item):
    google_lang = GoogleLanguage()
    news_keywords = []
    news_salience = []

    entities = google_lang.get_entities(news_item)
    for entity in entities:
        news_keywords.append(entity.name)
        news_salience.append(entity.salience)

    total_score = 0
    for i in range(len(tweet_keywords)):
        if tweet_keywords[i] in news_keywords:
            idx = news_keywords.index(tweet_keywords[i])
            total_score = 1 * news_salience[idx]

    normalized_score = total_score / sum(tweet_salience)

    return normalized_score


def relevance_score(tweet, news_item, key):
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
