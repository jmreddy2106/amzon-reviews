import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

import numpy as np

scored_reviews = pd.read_csv('./final_data.csv')

scored_reviews["valance_label"] = scored_reviews.loc[:, ["compound", "neg", "neu", "pos"]].idxmax(axis=1)

normalized_label = dict(scored_reviews['valance_label'].value_counts(normalize=True) * 100)
valance_val_per = pd.DataFrame()
valance_val_per['Sentiment_label'] = normalized_label.keys()
valance_val_per['%_of_Labels'] = normalized_label.values()

custom_colors = [plt.cm.tab20(np.arange(len(valance_val_per)))]

ax = valance_val_per.plot(kind='barh', legend=False, figsize=(12, 8), color=custom_colors)
ax.set_alpha(0.8)
ax.set_title("% of Labels of Polarity Score ", fontsize=18)
ax.set_xlabel("Count of Valance score", fontsize=18)
ax.set_xticks([10, 25, 50, 75, 100])

# create a list to collect the plt.patches data
totals = []

# find the values and append to listq
for i in ax.patches:
    totals.append(i.get_width())

# set individual bar lables using above list
for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
    ax.text(i.get_width() + .3, i.get_y() + .38,
            str(round((i.get_width()), 2)) + '%', fontsize=15, color='dimgrey')

# invert for largest on top
ax.invert_yaxis()
plt.savefig("Valance_Score.png")


reviews = scored_reviews["review"]
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

#
# ax = scored_reviews['valance_label'].value_counts().plot(kind='barh', figsize=(12,8))
# ax.set_alpha(0.8)
# ax.set_title(" Polarity Score labels", fontsize=18)
# ax.set_xlabel("Count Labels", fontsize=18)
# ax.set_xticks([100, 500, 1000, 1500, 2000, 3000, 4000, 5000])
#
# # create a list to collect the plt.patches data
# totals = []
#
# # find the values and append to list
# for i in ax.patches:
#     totals.append(i.get_width())
#
# # set individual bar lables using above list
# total = sum(totals)
# # set individual bar lables using above list
# for i in ax.patches:
#     # get_width pulls left or right; get_y pushes up or down
#     ax.text(i.get_width()+.3, i.get_y()+.38,
#             str(round((i.get_width()/total)*100, 2))+'%', fontsize=15, color='dimgrey')
#
# # invert for largest on top
# ax.invert_yaxis()
