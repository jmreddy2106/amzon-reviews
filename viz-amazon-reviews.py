import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.probability import FreqDist
from wordcloud import WordCloud, STOPWORDS
from collections import Counter

scored_reviews = pd.read_csv('./final_data.csv')
scored_reviews["valance_label"] = scored_reviews.loc[:, ["compound", "neg", "neu", "pos"]].idxmax(axis=1)

sb.countplot(x='valance_label', data=scored_reviews)
plt.xlabel("Valance Label", labelpad=14)
plt.ylabel("Count of labels", labelpad=14)
plt.title("Count of valance vs valance labels", y=1.02)
cnt_label = scored_reviews.valance_label.value_counts()
print(cnt_label)

for index, value in cnt_label.reset_index().iterrows():
    plt.text(index, value.valance_label, value.valance_label)
plt.savefig("Valance_Score.png")

# Distribution of Words
stopwords = stopwords.words('english')
stopwords = stopwords + [',', '(', ')', '“', '”', '.', '-', ':', '’', '~', '!', '`', '@', '#', '$', '%', '&', '*',
                         '+', '/', ';', '<', '>', '?', '[', ']', '{', '}', '_','•']

reviews = scored_reviews
reviews = reviews["review"]
word_dist = FreqDist()

# Tokenizing with punctuation marks
tk = TweetTokenizer()
word_frequencies = {}
for sent in reviews:
    for word in tk.tokenize(sent):
        word_lower = word.lower()
        if word not in stopwords:
            if word not in word_dist.keys():
                word_dist[word] = 1
                word_frequencies[word] = 1
            else:
                word_dist[word] += 1
                word_frequencies[word] += 1

print(word_dist.most_common(20))
# word_dist.plot(20, cumulative=False)

# Counter from Collections
k = Counter(word_frequencies)
# top 20 highest values
high = k.most_common(20)
x, y = zip(*high)
plt.figure(figsize=(12, 12))
plt.barh(x, y)
plt.xlabel("Frequency")
plt.ylabel("Words")

# for i, v in enumerate(y):
#     plt.text(v + 3, i + .25, str(v), color='blue', fontweight='bold')
plt.savefig('highest_freq.png')

sw_word_cloud = set(STOPWORDS)
set_of_words = ''

for sent in reviews:
    sent = str(sent)
    tokens = sent.split()
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
        set_of_words += " ".join(tokens) + " "

word_cloud = WordCloud(width=800, height=800,
                       max_words=100,
                       background_color='white',
                       stopwords=sw_word_cloud,
                       min_font_size=10).generate(set_of_words)

# plot the WordCloud image
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(word_cloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout(pad=0)

# Save the image in the img folder:
word_cloud.to_file("Amazon_review_wordcloud.png")

scored_reviews.to_csv('./amazon-review-valance-label.csv', index=False)
