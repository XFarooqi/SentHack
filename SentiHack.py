# This example requires environment variables named "LANGUAGE_KEY" and "LANGUAGE_ENDPOINT"
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import os
language_key = os.environ.get('LANGUAGE_KEY')
language_endpoint = os.environ.get('LANGUAGE_ENDPOINT')

# Authenticate the client using your key and endpoint

def authenticate_client():
    ta_credential = AzureKeyCredential(language_key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=language_endpoint,
        credential=ta_credential)
    return text_analytics_client


client = authenticate_client()

# Example method for detecting sentiment and opinions in text


def sentiment_analysis_with_opinion_mining_example(client):

    documents = [
        """There are a few potential drawbacks and bad things in the MLH hackathons that students should be aware of.

Limited Availability: MLH hackathons are only hosted in certain regions, and may not be available to all students. This can limit access to these opportunities for those who live in areas where these events are not held.

Cost: Attending MLH hackathons can be expensive, especially for students who have to cover travel and accommodation expenses. This may make these events inaccessible for some students.

Lack of Diversity: Although MLH is committed to promoting diversity and inclusion, some students may still feel like they are not well-represented at these events. For example, some groups may feel like they are not adequately represented in terms of gender, race, or socioeconomic status.

Intensity: MLH hackathons can be intense and fast-paced, which can be challenging for some students. This may make these events more suitable for experienced coders and less accessible for those who are just starting out.

Limited Focus: MLH hackathons often focus on specific technologies or programming languages, which may not align with all students' interests or career goals. This can make these events less appealing or relevant for some students.
"""]

    result = client.analyze_sentiment(documents, show_opinion_mining=True)
    doc_result = [doc for doc in result if not doc.is_error]

    positive_reviews = [
        doc for doc in doc_result if doc.sentiment == "Positive"]
    negative_reviews = [
        doc for doc in doc_result if doc.sentiment == "Negative"]

    positive_mined_opinions = []
    mixed_mined_opinions = []
    negative_mined_opinions = []

    for document in doc_result:
        print("Document Sentiment: {}".format(document.sentiment))
        print("Overall scores: Positive={0:.2f}; Neutral={1:.2f}; Negative={2:.2f} \n".format(
            document.confidence_scores.positive,
            document.confidence_scores.neutral,
            document.confidence_scores.negative,
        ))
        for sentence in document.sentences:
            print("Sentence: {}".format(sentence.text))
            print("Sentence sentiment: {}".format(sentence.sentiment))
            print("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
                sentence.confidence_scores.positive,
                sentence.confidence_scores.neutral,
                sentence.confidence_scores.negative,
            ))
            for mined_opinion in sentence.mined_opinions:
                target = mined_opinion.target
                print("......'{}' target '{}'".format(
                    target.sentiment, target.text))
                print("......Target score:\n......Positive={0:.2f}\n......Negative={1:.2f}\n".format(
                    target.confidence_scores.positive,
                    target.confidence_scores.negative,
                ))
                for assessment in mined_opinion.assessments:
                    print("......'{}' assessment '{}'".format(
                        assessment.sentiment, assessment.text))
                    print("......Assessment score:\n......Positive={0:.2f}\n......Negative={1:.2f}\n".format(
                        assessment.confidence_scores.positive,
                        assessment.confidence_scores.negative,
                    ))
            print("\n")
        print("\n" "\n""\n""\n""\n")

    for document in doc_result:
        print("Document Sentiment: {}".format(document.sentiment))
        print("Overall scores: Positive={0:.2f}; Neutral={1:.2f}; Negative={2:.2f} \n".format(
            document.confidence_scores.positive,
            document.confidence_scores.neutral,
            document.confidence_scores.negative,
        ))


sentiment_analysis_with_opinion_mining_example(client)
