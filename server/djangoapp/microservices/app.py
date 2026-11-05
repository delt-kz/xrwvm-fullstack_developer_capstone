import os
from pathlib import Path
import nltk
from flask import Flask, jsonify
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.data.path.insert(0, str(Path(__file__).parent))
sia = SentimentIntensityAnalyzer()
app = Flask(__name__)
@app.get('/')
def home():
    return jsonify(service='VADER sentiment analyzer',status='ok')
@app.get('/analyze/<path:input_txt>')
def analyze_sentiment(input_txt):
    score = sia.polarity_scores(input_txt)['compound']
    sentiment = 'positive' if score >= 0.05 else 'negative' if score <= -0.05 else 'neutral'
    return jsonify(sentiment=sentiment,compound=score)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(os.getenv('PORT','5050')))
