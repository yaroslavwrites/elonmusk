import nltk
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# Ensure necessary NLTK datasets are downloaded
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

lemmatizer = WordNetLemmatizer()

def nltk_tag_to_wordnet_tag(nltk_tag):
    """Map NLTK POS tag to first character used by WordNetLemmatizer"""
    tag = {
        'N': wordnet.NOUN,
        'V': wordnet.VERB,
        'R': wordnet.ADV,
        'J': wordnet.ADJ
    }.get(nltk_tag[0], wordnet.NOUN)
    return tag

def preprocess_and_lemmatize(tweet):
    # Convert to lowercase
    tweet = tweet.lower()

    # Expand common contractions
    contractions = {
        "ain't": "are not",
        "aren't": "are not",
        "can't": "cannot",
        "can't've": "cannot have",
        "could've": "could have",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hadn't've": "had not have",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'd've": "he would have",
        "he'll": "he will",
        "he's": "he is",
        "how'd": "how did",
        "how'll": "how will",
        "how's": "how is",
        "i'd": "i would",
        "i'll": "i will",
        "i'm": "i am",
        "i've": "i have",
        "isn't": "is not",
        "it'd": "it would",
        "it'll": "it will",
        "it's": "it is",
    }
    
    for contraction, expansion in contractions.items():
        tweet = tweet.replace(contraction, expansion)

    # Remove URLs, mentions, hashtags, numbers, punctuation, and special characters
    tweet = re.sub(r'http\S+|www\S+|https\S+', '', tweet, flags=re.MULTILINE)
    tweet = re.sub(r'\@\w+|\#', '', tweet)
    tweet = re.sub(r'[^a-zA-Z\s]', '', tweet)

    tokens = nltk.word_tokenize(tweet)
    pos_tags = nltk.pos_tag(tokens)

    # Remove stopwords, apply lemmatization, and filter short tokens
    tokens = [lemmatizer.lemmatize(token, nltk_tag_to_wordnet_tag(pos)) for token, pos in pos_tags if token not in stopwords.words('english') and len(token) > 1]

    # Return the cleaned and lemmatized tweet
    return " ".join(tokens)

# Load tweets from "combined.csv"
df = pd.read_csv("combined_tweets/combined.csv")

# Process each tweet
df["processedContent"] = df["rawContent"].apply(preprocess_and_lemmatize)

# Save the processed tweets and date in a new CSV file
df[["date", "processedContent"]].to_csv("combined_tweets/processed_final.csv", index=False)
