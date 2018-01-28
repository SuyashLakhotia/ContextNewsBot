from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


ENTITY_TYPES = ["UNKNOWN", "PERSON", "LOCATION", "ORGANIZATION", "EVENT", "WORK_OF_ART", "CONSUMER_GOOD",
                "OTHER"]
IMP_ENTITY_IDX = [1, 2, 3, 4, 5, 6]
REALLY_IMP_ENTITY_IDX = [1, 2, 3, 4]


class GoogleLanguage(object):

    def __init__(self):
        self.client = language.LanguageServiceClient()

    def get_entities(self, text):
        document = types.Document(content=text,
                                  type=enums.Document.Type.PLAIN_TEXT)
        response = self.client.analyze_entities(document=document,
                                                encoding_type=enums.EncodingType.UTF32)

        for entity in response.entities:
            if entity.mentions[0].type == enums.EntityMention.Type.COMMON:
                entity.salience = entity.salience * 0.5

        return response.entities

    def get_entities_sentiment(self, text):
        document = types.Document(content=text,
                                  type=enums.Document.Type.PLAIN_TEXT)
        response = self.client.analyze_entity_sentiment(document=document,
                                                        encoding_type=enums.EncodingType.UTF32)
        return response.entities

    def get_document_sentiment(self, text):
        document = types.Document(content=text,
                                  type=enums.Document.Type.PLAIN_TEXT)
        sentiment = self.client.analyze_sentiment(document=document,
                                                  encoding_type=enums.EncodingType.UTF32).document_sentiment
        return sentiment
