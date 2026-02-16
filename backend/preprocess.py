import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize

try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

STOP_WORDS = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    tokens = wordpunct_tokenize(text)

    cleaned_tokens = [
        word for word in tokens
        if word not in STOP_WORDS
    ]

    return cleaned_tokens
