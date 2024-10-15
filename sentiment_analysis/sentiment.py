from textblob import TextBlob

def analyze_sentiment(comments):
    sentiments = []
    for comment in comments:
        analysis = TextBlob(comment).sentiment.polarity
        sentiments.append('positive' if analysis > 0 else 'negative' if analysis < 0 else 'neutral')
    return sentiments

