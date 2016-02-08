import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
import Quandl

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
# Création d'un ratio pour les tweets, positifs/total
common['ratio'] = 0
common['ratio'] = np.round(
    common['positif'] / (common['positif'] + common['negatif']), 2)

common.to_csv('data.csv')

# Affichage du graphique
fig, ax1 = plt.subplots()

t = common.cours
s1 = common.index
ax1.plot(s1, t, 'b-')
# ax1.axis.set_major_formatter(mdates.DateFormatter('%Y/%d/%m'))
ax1.set_xlabel('date')
# Make the y-axis label and tick labels match the line color.
ax1.set_ylabel('bitcoin', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')

ax2 = ax1.twinx()
s2 = common.ratio
ax2.plot(s2, t, 'r-')
ax2.set_ylabel('ratio pos/neg', color='r')
for tl in ax2.get_yticklabels():
    tl.set_color('r')
plt.show()
