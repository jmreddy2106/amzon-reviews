import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import emoji
import re


def sentence_score(rs):
    review_score = SentimentIntensityAnalyzer()
    compound.append(review_score.polarity_scores(rs)['compound'])
    neg.append(review_score.polarity_scores(rs)['neg'])
    neu.append(review_score.polarity_scores(rs)['neu'])
    pos.append(review_score.polarity_scores(rs)['pos'])


pd.set_option('display.max_colwidth', -1)

reviews = pd.read_csv('./amazon-reviews.csv')
review_sentences = reviews["Description"]

compound = []
pos = []
neu = []
neg = []
clean_sent = []

# Ignoring the urls from text
url_reg = r'[a-z]*[:.]+\S+'

for sentence in review_sentences:
    try:
        sentence = re.sub(emoji.get_emoji_regexp(), r"", sentence)
        sentence = re.sub(url_reg, '', sentence)
        if sentence and not sentence == 'NULL':
            clean_sent.append(sentence)
            sentence_score(sentence)
    except re.error:
        print(sentence)

final_reviews = pd.DataFrame({'compound': compound, 'neg': neg, 'neu': neu, 'pos': pos, 'review': clean_sent})
final_reviews.to_csv('./final_data.csv', index=False)

print('Polarity Score is Calculated...!')
