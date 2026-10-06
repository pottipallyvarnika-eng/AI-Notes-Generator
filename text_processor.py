import re

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer


def clean_text(text):
    text = text.replace("\x00", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_into_sentences(text):
    sentences = re.split(r"(?<=[.!?])\s+", text)

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def extract_keywords(text, number=10):

    if not text.strip():
        return []

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=number
        )

        matrix = vectorizer.fit_transform([text])

        words = vectorizer.get_feature_names_out()

        return list(words)

    except Exception:
        return []


def simple_summary(text, sentence_count=5):

    sentences = split_into_sentences(text)

    if len(sentences) <= sentence_count:
        return " ".join(sentences)

    return " ".join(sentences[:sentence_count])