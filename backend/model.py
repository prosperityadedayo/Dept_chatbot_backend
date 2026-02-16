import json
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from preprocess import preprocess_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "..", "data", "training_data.json")
MODEL_PATH = os.path.join(BASE_DIR, "chatbot_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")


def load_training_data(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["intents"]


def prepare_training_data(intents):
    texts = []
    labels = []

    for intent in intents:
        tag = intent["tag"]
        for pattern in intent["patterns"]:
            tokens = preprocess_text(pattern)
            texts.append(" ".join(tokens))
            labels.append(tag)

    return texts, labels


def train_model():
    intents = load_training_data(DATA_PATH)
    texts, labels = prepare_training_data(intents)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    model = MultinomialNB()
    model.fit(X, labels)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    print("Model training complete. Files saved successfully.")


if __name__ == "__main__":
    train_model()
