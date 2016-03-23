from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF
import pandas as pd

n_features = 2000
n_topics = 10
n_top_words = 10

# Load the 20 newsgroups dataset and vectorize it. We use a few heuristics
# to filter out useless terms early on: the posts are stripped of headers,
# footers and quoted replies, and common English words, words occurring in
# only one document or in at least 95% of the documents are removed.

tweets = pd.read_csv('data/dataframes/allTweets.csv')
corpus = tweets['tweet']

vectorizer = CountVectorizer(min_df=1, stop_words='english')
tfidf = vectorizer.fit_transform(corpus)

# Fit the NMF model
nmf = NMF(n_components=n_topics, random_state=1).fit(tfidf)

feature_names = vectorizer.get_feature_names()

for topic_idx, topic in enumerate(nmf.components_):
    print("Topic #%d:" % topic_idx)
    print(" ".join([feature_names[i]
                    for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()
