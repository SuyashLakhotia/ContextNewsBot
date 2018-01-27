import requests

import paralleldots
from google_language import GoogleLanguage
from google_language import REALLY_IMP_ENTITY_IDX

from news_utils import pretty_print_news


def get_relevant_news(tweet, tweet_keywords, tweet_salience, news_articles, threshold):
    relevant_news_articles = []

    for item in news_articles:
        relevance_score = relevance_score_google(tweet, tweet_keywords, tweet_salience,
                                                 item['title'] + ". " + item['description'])
        item["relevance_score"] = relevance_score
        if relevance_score >= threshold:
            relevant_news_articles.append(item)

    relevant_news_articles.sort(key=lambda x: x['relevance_score'], reverse=True)
    return relevant_news_articles[:3]


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

            if entities[idx].type in REALLY_IMP_ENTITY_IDX:
                total_score += (news_salience[idx] * 1.5) * min(3, len(entities[idx].mentions))
            else:
                total_score += news_salience[idx] * min(3, len(entities[idx].mentions))

    normalized_score = total_score / sum(tweet_salience)

    return normalized_score


def get_relevant_news_tfidf(tweet, news_articles, threshold=0.5):
    import gensim
    from nltk.tokenize import word_tokenize

    news_articles_text = [item['title'] + ". " + item['description'] for item in news_articles]
    news_articles_tokenized = [[w.lower() for w in word_tokenize(item)]
                               for item in news_articles_text]

    dictionary = gensim.corpora.Dictionary(news_articles_tokenized)
    corpus = [dictionary.doc2bow(item_tokenized) for item_tokenized in news_articles_tokenized]
    tf_idf = gensim.models.TfidfModel(corpus)
    sims = gensim.similarities.Similarity('', tf_idf[corpus],
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


def get_relevant_news_cosine(tweet, news_articles, threshold=0.5):
    import spacy

    nlp = spacy.load('en_core_web_sm')  # need to download: python -m spacy download en_core_web_sm/_md/_lg
    news_articles_vectors = [nlp(item['title'] + ". " + item['description']) for item in news_articles]
    tweet_vector = nlp(tweet)

    relevant_news_articles = []
    for idx, item in enumerate(news_articles_vectors):
        similarity_score = tweet_vector.similarity(item)
        if similarity_score >= threshold:
            news_articles[idx]["relevance_score"] = similarity_score
            relevant_news_articles.append(news_articles[idx])

    return relevant_news_articles


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
