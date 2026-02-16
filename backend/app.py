from flask import Flask, request, jsonify, render_template
import pickle
import json
import os
import random
from preprocess import preprocess_text

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "chatbot_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "training_data.json")

# Load model and vectorizer
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

with open(DATA_PATH, "r", encoding="utf-8") as f:
    intents_data = json.load(f)["intents"]


# ---------- ROUTES ----------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"reply": "Invalid request"}), 400

    user_message = data["message"]

    tokens = preprocess_text(user_message)
    cleaned_text = " ".join(tokens)

    X = vectorizer.transform([cleaned_text])
    predicted_tag = model.predict(X)[0]

    response = "I'm not sure about that. Please contact the department."

    for intent in intents_data:
        if intent["tag"] == predicted_tag:
            response = random.choice(intent["responses"])
            break

    return jsonify({"reply": response})


if __name__ == "__main__":
    app.run(debug=True)
