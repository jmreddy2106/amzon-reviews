import pandas as pd
import emoji
import re
import seaborn as sb
from nltk import FreqDist
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from Contractions import custum_contractions


def Preprocess(review):

    try:
        sent = re.sub(emoji.get_emoji_regexp(), r"", review)
        sent = re.sub('http[s]?://\S+', '', sent)
        sent = re.sub('/-', ' ', sent)
        sent = re.sub('•', '', sent)
        sent = re.sub('--AA', '', sent)
        sent = re.sub('/', ' ', sent)
        sent = re.sub('-', ' ', sent)
        sent = re.sub('!!!!', ' ', sent)
        sent = re.sub('WM126', ' ', sent)
        sent = re.sub('::', ' ', sent)
        sent = re.sub("ossssmmmmmmmmmmm", ' ', sent)
        sent = re.sub(r"\.(?=\S)", ". ", sent)
        sent = re.sub('``', ' ', sent)
        sent = re.sub("''", ' ', sent)
        sent = re.sub("…", ' ', sent)
        sent = re.sub('~', ' ', sent)
        sent = re.sub('✓',' ', sent)

        sent = custum_contractions(sent)
        if len(sent) > 0:
            clean_sent.append(sent)
    except re.error:
        print(review)



reviews_data = pd.read_csv('./amazon-reviews.csv', error_bad_lines=False)
review_sentences = reviews_data["Description"].dropna()





clean_sent = []

stop_words = stopwords.words('english')
stop_words = stop_words + [',', '(', ')', '"', '', '.', ':', '’', '~', '!', '`', '@', '#','OEM','l','n','h','w',''
                           '$', '%', '&', '*', '+', ';', '<', '>', '?', '[', ']','WM126','pc',
                           '{', '}', '_', '....', '..', '.....', '+ve', '-ve','x',
                           'ossssmmmmmmmmmmm', '""', '/-', '::', '(', ')', 'apx.', '..', 'Wow!', ':/', 'w/o',
                            'OMG', 'gr8','..........', 's/n', 'p/n', 'pro4', ',', 'qa', 'Pls', 'hmm', 'Awww', '/',"''",'``']

for sentence in review_sentences:
    Preprocess(sentence)

word_frequencies = {}
for sent in clean_sent:
    for word in word_tokenize(sent):
            word_lower = word.lower()
            if word_lower not in stop_words and not word_lower.isdigit():
                if word_lower not in word_frequencies.keys():
                    word_frequencies[word_lower] = 1
                else:
                    word_frequencies[word_lower] += 1
sorted_word_freq = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)

print(sorted_word_freq)

# reviews = [remove_stopwords(r.split()) for r in clean_sent]
# reviews = [r.lower() for r in reviews]
# print(reviews)

# # function to plot most frequent terms
# def freq_words(x, terms=20):
#     all_words = ' '.join([text for text in x])
#     all_words = all_words.split()
#
#     fdist = FreqDist(all_words)
#     words_df = pd.DataFrame({'word': list(fdist.keys()), 'count': list(fdist.values())})
#
#     # selecting top 20 most frequent words
#     d = words_df.nlargest(columns="count", n=terms)
#     plt.figure(figsize=(20, 5))
#     ax = sb.barplot(data=d, x="word", y="count")
#     ax.set(ylabel='Count')
#     plt.show()
#
#
# freq_words(reviews, 20)
