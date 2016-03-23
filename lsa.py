import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

tweets = pd.read_csv('data/dataframes/allTweets.csv').sample(10000)
corpus = tweets['tweet']

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(corpus)

#print(vectorizer.get_feature_names())

df = pd.DataFrame(X.toarray(), index=tweets.index,
                  columns=vectorizer.get_feature_names())

import prince

pca = prince.PCA(df, components=2)
# PCA summary
pca.summary()
# Plot the inertia percentages
#pca.plot_inertia(threshold=0.8, kind='mpl')
# Plot the row projections
pca.plot_rows(axis=[0, 1], show_names=False, kind='mpl')
# Plot the variable/component correlation circle
#pca.plot_correlation_circle(axis=[0, 1], kind='mpl')
