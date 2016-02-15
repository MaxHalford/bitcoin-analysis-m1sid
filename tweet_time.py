import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
import Quandl
import seaborn

# Récupération des tweets positifs
dfp = pd.read_csv('data/timestamps/positifs.txt', header=None, index_col=0)
dfp['value'] = 1
# Conversion de l'index en datetime
dfp.index = pd.to_datetime(dfp.index, unit='ms')
# On compte les tweets positifs par date
dfp = dfp.groupby((dfp.index.date)).count()
dfp.index = pd.to_datetime(dfp.index, unit='ms')

# Affichage du graphique
# dfp.plot()
# plt.show()


# Récupération des tweets négatifs
dfn = pd.read_csv('data/timestamps/negatifs.txt', header=None, index_col=0)
dfn['value'] = 1
# Conversion de l'index en datetime
dfn.index = pd.to_datetime(dfn.index, unit='ms')
# On compte les tweets négatifs par date
dfn = dfn.groupby((dfn.index.date)).count()
dfn.index = pd.to_datetime(dfn.index, unit='ms')

# Affichage du graphique
# dfn.plot()
# plt.show()

# Cours du bitcoin
value = Quandl.get('BCHAIN/MKPRU', authtoken='ri21BpjKtw3SVkCYWpKw',
                   collapse='daily')
value.index = pd.to_datetime(value.index, unit='ms')

# Mise en commun
keys = ['positif', 'negatif', 'cours']
common = pd.concat([dfp, dfn, value], axis=1, keys=keys)
common['cours'] = np.round(common['cours'], 2)

# On renomme les colonnes
common.columns = keys

# Affichage des tweets positifs vs. négatifs
common.loc[:, ['positif', 'negatif']].plot(
    title="Évolution de la nature des tweets liés à \"bitcoin\" de 2009 à aujourd'hui")
# plt.show()


def compute_ratio(df):
    ''' Création d'un ratio pour les tweets, positifs/total '''
    df['ratio'] = np.round(
        df['positif'] / (df['positif'] + df['negatif']), 2)
    df['ratio'] = np.nan_to_num(df['ratio'])
    return df

common['ratio'] = 0
common = compute_ratio(common)

common.to_csv('data/common_daily.csv')

# Visualisation du ratio
common.loc[:, ['ratio']].plot(kind='line',
                              title="Évolution du ratio de tweets positifs liés à \"bitcoin\" de 2009 à aujourd'hui")
# plt.show()

# Cours du bitcoin suivant le ratio
common.plot(secondary_y=['positif', 'negatif'],
            title="Évolution du bitcoin de 2009 à aujourd'hui")
# plt.show()

# On supprime les colonnes que l'on ne souhaite pas afficher.
common.loc[:, ['ratio', 'cours']].plot(secondary_y=['ratio'],
                                       title="Évolution du bitcoin de 2009 à aujourd'hui")
# plt.show()

# Est-ce que quand le ratio tweets +/- augmente, implique que dans un
# espace de temps variable futur que le cours du bitcoin augmente ?

# On effectue une corrélation de rang décalée

# Sens ratio-cours


def corr_ratio_cours(df, scale=1):
    df.cours = df.cours.shift(scale)
    corr_rang = df['ratio'].corr(df['cours'], method='spearman')
    return corr_rang

# pd.Series([corr_ratio_cours(common, scale=i)
#            for i in range(30)]).plot(title="ratio => cours (par jour)", ylim=(0, 1))
# plt.show()

# Sens cours-ratio


def corr_cours_ratio(df, scale=1):
    df.cours = df.cours.shift(scale)
    corr_rang = df['cours'].corr(df['ratio'], method='spearman')
    return corr_rang

# pd.Series([corr_cours_ratio(common, scale=i)
#            for i in range(30)]).plot(title="cours => ratio (par jour)", ylim=(0, 1))
# plt.show()

# Il semblerait qu'il faille étudier davantage la corrélation par semaine
# entre le cours du bitcoin et le ratio de tweets positifs / tweets totaux

# Cours du bitcoin
value = Quandl.get('BCHAIN/MKPRU', authtoken='ri21BpjKtw3SVkCYWpKw',
                   collapse='weekly')
value.index = pd.to_datetime(value.index, unit='ms')

# Mise en commun
keys = ['positif', 'negatif', 'cours']
common = pd.concat([dfp, dfn, value], axis=1, keys=keys)
common['cours'] = np.round(common['cours'], 2)

# On renomme les colonnes
common.columns = keys
# Création d'un ratio pour les tweets, positifs/total
common = compute_ratio(common)

common.to_csv('data/common_weekly.csv')


# Sens ratio-cours

# pd.Series([corr_ratio_cours(common, scale=i)
#            for i in range(14)]).plot(title="ratio => cours (par semaine)", ylim=(0, 1))
# plt.show()


# Sens cours-ratio

# pd.Series([corr_cours_ratio(common, scale=i)
#            for i in range(14)]).plot(title="cours => ratio (par semaine)", ylim=(0, 1))
# plt.show()
