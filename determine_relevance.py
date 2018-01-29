import requests

from google_language import GoogleLanguage
from google_language import REALLY_IMP_ENTITY_IDX

from news_utils import pretty_print_news


google_lang = GoogleLanguage()


def get_relevant_news(tweet, tweet_entities, news_articles, threshold):
    relevant_news_articles = []

    for item in news_articles:
        relevance_score = relevance_score_google(tweet, tweet_entities,
                                                 item["title"] + ". " + item["description"])
        item["relevance_score"] = relevance_score
        if relevance_score >= threshold:
            relevant_news_articles.append(item)

    relevant_news_articles.sort(key=lambda x: x["relevance_score"], reverse=True)

    final_articles = []
    sources_covered = []
    for item in relevant_news_articles:
        if item["source"]["id"] not in sources_covered:
            final_articles.append(item)
            sources_covered.append(item["source"]["id"])

    for item in final_articles[:3]:
        news_item = item["title"] + ". " + item["description"]
        sentiment = google_lang.get_document_sentiment(news_item)
        item["sentiment_score"] = sentiment.score

    pretty_print_news(final_articles[:3])

    return final_articles[:3]


def relevance_score_google(tweet, tweet_entities, news_item):
    news_entities_names = []

    entities = google_lang.get_entities(news_item)
    for entity in entities:
        news_entities_names.append(entity.name)

    total_score = 0
    for i in range(len(tweet_entities)):
        if tweet_entities[i].name in news_entities_names:
            idx = news_entities_names.index(tweet_entities[i].name)

            if entities[idx].type in REALLY_IMP_ENTITY_IDX:
                total_score += (entities[idx].salience * 1.5) * min(3, len(entities[idx].mentions))
            else:
                total_score += entities[idx].salience * min(3, len(entities[idx].mentions))

    return total_score


def get_relevant_news_tfidf(tweet, news_articles, threshold=0.5):
    import gensim
    from nltk.tokenize import word_tokenize

    news_articles_text = [item["title"] + ". " + item["description"] for item in news_articles]
    news_articles_tokenized = [[w.lower() for w in word_tokenize(item)]
                               for item in news_articles_text]

    dictionary = gensim.corpora.Dictionary(news_articles_tokenized)
    corpus = [dictionary.doc2bow(item_tokenized) for item_tokenized in news_articles_tokenized]
    tf_idf = gensim.models.TfidfModel(corpus)
    sims = gensim.similarities.Similarity("", tf_idf[corpus],
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

    nlp = spacy.load("en_core_web_sm")  # need to download: python -m spacy download en_core_web_sm/_md/_lg
    news_articles_vectors = [nlp(item["title"] + ". " + item["description"]) for item in news_articles]
    tweet_vector = nlp(tweet)

    relevant_news_articles = []
    for idx, item in enumerate(news_articles_vectors):
        similarity_score = tweet_vector.similarity(item)
        if similarity_score >= threshold:
            news_articles[idx]["relevance_score"] = similarity_score
            relevant_news_articles.append(news_articles[idx])

    return relevant_news_articles
