import pandas as pd
import seaborn
import prince

# Load a dataframe
url = 'http://maxhalford.com/data/datasets/prince/decathlon.csv'
df = pd.read_csv(url, index_col=0)
# Compute the PCA
pca = prince.PCA(df, ignored=['Rank', 'Points'])
# PCA summary
pca.summary()
# Plot the inertia percentages
pca.plot_inertia(threshold=0.8, kind='mpl')
# Plot the row projections
pca.plot_rows(axis=[0, 1], by='Competition', kind='mpl')
# Plot the variable/component correlation circle
pca.plot_correlation_circle(axis=[0, 1], kind='mpl')
