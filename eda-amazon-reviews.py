import pandas as pd
import matplotlib.pyplot as plt
from nltk.probability import FreqDist
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import numpy as np



scored_reviews = pd.read_csv('./amazon-review-valance-label.csv')
dim = scored_reviews.shape
print("Dimension of the Dataset => ", dim)

class_gb = scored_reviews.valance_label.value_counts()
print("Class distribution => ", class_gb)

# scored_reviews['review_len'] = scored_reviews['review'].astype(str).apply(len)
# scored_reviews['word_count'] = scored_reviews['review'].apply(lambda x: len(str(x).split()))
#
# scored_reviews.to_csv('./polarity_score.csv', index=False)

# Distribution of Words
stopwords = stopwords.words('english')
stopwords = stopwords + [',', '(', ')', '“', '”', '.', '-', ':', '’', '~', '!', '`', '@', '#', '$', '%', '&', '*',
                         '+', '/', ';', '<', '>', '?', '[', ']', '{', '}', '_', '•']

reviews = scored_reviews
reviews = reviews["review"]
# word_dist = FreqDist()

# # Tokenizing with punctuation marks
tk = TweetTokenizer()
# word_frequencies = {}
# for sent in reviews:
#     for word in tk.tokenize(sent):
#         word_lower = word.lower()
#         if word not in stopwords:
#             if word not in word_frequencies.keys():
#                 # word_dist[word] = 1
#                 word_frequencies[word] = 1
#             else:
#                 # word_dist[word] += 1
#                 word_frequencies[word] += 1
#
# # print(word_dist.most_common(20))
# # word_dist.plot(20, cumulative=False)
#
# # Counter from Collections
# k = Counter(word_frequencies)
# # top 20 highest values
# high = k.most_common(20)
# most_20_words = pd.DataFrame(high, columns=["Word", "Frequency_cnt"])
# most_20_words.set_index('Word', inplace=True)
#
# print(most_20_words)
#
# custom_colors = [plt.cm.tab20(np.arange(len(most_20_words)))]
#
# top_20 = most_20_words.plot(kind='barh', legend=False, figsize=(8, 8), color=custom_colors)
# top_20.set_alpha(0.8)
# top_20.set_title(" Top 20 - most common frequent words ", fontsize=18)
# top_20.set_xlabel(" Count of most common words ", fontsize=18)
# top_20.set_xticks([100, 200, 400, 600, 800, 1000, 1200])
#
# # create a list to collect the plt.patches data
# totals_20 = []
#
# # find the values and append to listq
# for i in top_20.patches:
#     totals_20.append(i.get_width())
#
# # set individual bar lables using above list
# for i in top_20.patches:
#     # get_width pulls left or right; get_y pushes up or down
#     top_20.text(i.get_width() + .3, i.get_y() + .38,
#             str(round((i.get_width()), 2)), fontsize=15, color='dimgrey')
#
# # invert for largest on top
# top_20.invert_yaxis()
# plt.savefig('highest_20_freq.png')

from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

porter=PorterStemmer()

# for sentence in reviews:
#     for word in tk.tokenize(sentence):
#         word_lower = word.lower()
#         if word not in stopwords:
#             print("Lemma for {} is {}".format(word_lower, wordNet_lemma.lemmatize(word_lower)))
def stemSentence(sentence):
    token_words = tk.tokenize(sentence)
    stem_sentence = []
    for word in token_words:
        stem_sentence.append(porter.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)
for sentence in reviews:
    print(sentence)
    print("Stemmed sentence")
    x = stemSentence(sentence)
    print(x)

# class_label = []
#
# valance_label = scored_reviews["valance_label"]

# for lbl in valance_label:
#     if lbl in ["compound", "neu"]:
#         class_label.append("pos")
#     elif lbl in "neg":
#         class_label.append("neg")
#     else:
#         class_label.append("pos")
#
# temp_class = pd.DataFrame({"class_label": class_label})
# print(temp_class.class_label.value_counts())
