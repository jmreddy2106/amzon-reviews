import pandas as pd
import matplotlib.pyplot as plt
from nltk.probability import FreqDist
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import seaborn as sb
from sklearn.feature_extraction.text import CountVectorizer

scored_reviews = pd.read_csv('./amazon-review-valance-label.csv')
dim = scored_reviews.shape
print("Dimension of the Dataset => ", dim)

class_gb = scored_reviews.valance_label.value_counts()
print("Class distribution => ", class_gb)

# Distribution of Words
stopwords = stopwords.words('english')
stopwords = stopwords + [',', '(', ')', '“', '”', '.', '-', ':', '’', '~', '!', '`', '@', '#', '$', '%', '&', '*',
                         '+', '/', ';', '<', '>', '?', '[', ']', '{', '}', '_', '•']

reviews = scored_reviews
reviews = reviews["review"]
# word_dist = FreqDist()

# # Tokenizing with punctuation marks
tk = TweetTokenizer()
word_frequencies = {}
for sent in reviews:
    for word in tk.tokenize(sent):
        word_lower = word.lower()
        if word not in stopwords:
            if word not in word_frequencies.keys():
                # word_dist[word] = 1
                word_frequencies[word] = 1
            else:
                # word_dist[word] += 1
                word_frequencies[word] += 1

# print(word_dist.most_common(20))
# word_dist.plot(20, cumulative=False)

# Counter from Collections
k = Counter(word_frequencies)
# top 20 highest values
high = k.most_common(20)
most_20_words = pd.DataFrame(high, columns=["Word", "Frequency_cnt"])
most_20_words.set_index('Word', inplace=True)

print(most_20_words)

custom_colors = [plt.cm.tab20(np.arange(len(most_20_words)))]
plt.figure()
top_20 = most_20_words.plot(kind='barh', legend=False, figsize=(8, 8), color=custom_colors)
top_20.set_alpha(0.8)
top_20.set_title(" Top 20 - most common frequent words ", fontsize=20)
top_20.set_xlabel(" Count of most common words ", fontsize=18)
top_20.set_xticks([100, 200, 400, 600, 800, 1000, 1200])

# create a list to collect the plt.patches data
totals_20 = []

# find the values and append to listq
for i in top_20.patches:
    totals_20.append(i.get_width())

# set individual bar lables using above list
for i in top_20.patches:
    # get_width pulls left or right; get_y pushes up or down
    top_20.text(i.get_width() + .3, i.get_y() + .38,
                str(round((i.get_width()), 2)), fontsize=18, color='dimgrey')

# invert for largest on top
top_20.invert_yaxis()

plt.savefig('highest_20_freq.png')

############## Lemmatization Module ######################
wordNet_lemma = WordNetLemmatizer()
porter = PorterStemmer()

lemma_word = []
original_word = []
filtered_sentence = []

# print("{0:20}{1:20}".format("Word","Lemma"))
for sentence in reviews:
    for w in tk.tokenize(sentence):
        w_lower = w.lower()
        if w_lower not in stopwords:
            filtered_sentence.append(w_lower)

for w in filtered_sentence:
    original_word.append(w)
    word1 = wordNet_lemma.lemmatize(w, pos="n")  # n - noun
    word2 = wordNet_lemma.lemmatize(word1, pos="v")  # v - verb
    word3 = wordNet_lemma.lemmatize(word2, pos=("a"))  # a - adjective
    lemma_word.append(word3)

    # print("{0:20}{1:20}".format(w, word3))

lemm = pd.DataFrame({"Original_word": original_word, "Lemmatized_words": lemma_word})
lemm.to_csv("./Lemmatized_Amazon_reviews.csv", index=False)


# Get top Ngrams of corpus
def get_top_ngram(corpus, n=None):
    vec = CountVectorizer(ngram_range=(n, n)).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx])
                  for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:10]


# For Bigrams
top_n_bi_grams = get_top_ngram(reviews, n=2)
x_bi, y_bi = map(list, zip(*top_n_bi_grams))
bi_gram = plt.figure(figsize=(15,10))
bi_gram.suptitle(" Top 10 - Bigrams ", fontsize=20)
plt.xlabel("Frequency of Bigrams", fontsize=18)
plt.ylabel("Bigrams", fontsize=18)
bi = sb.barplot(x=y_bi, y=x_bi)
bi_gram.savefig("top_10_Bigrams.png")

# For Trigrams
top_n_tri_grams = get_top_ngram(reviews, n=3)
x_tri, y_tri = map(list, zip(*top_n_tri_grams))
tri_gram = plt.figure(figsize=(15, 10))
tri_gram.suptitle(" Top 10 - Trigrams ", fontsize=20)
plt.xlabel("Frequency of Trigrams", fontsize=18)
plt.ylabel("Trigrams", fontsize=18)
tri = sb.barplot(x=y_tri, y=x_tri)
tri_gram.savefig("top_10_Trigrams.png")

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
