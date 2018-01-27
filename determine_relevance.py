import paralleldots


class RelevanceDeterminer(object):
	def __init__(self, threshold):
		self.threshold = threshold

		paralleldots.set_api_key("siQChQ9PVPRs8Gm0HDawsqscverucbEq77zNBZpNXI8")

	def get_relevant_news(tweet, news_set, threshold=self.threshold):
		relevant_news_set = []
		for item in news_set:
			if _relevance_score(tweet, item) >= threshold:
				relevant_news_set.append(item):

	def _relevance_score(tweet, news_item):
		# TODO depends on structure of news_item
		paralleldots.similarity(tweet, news_item)


