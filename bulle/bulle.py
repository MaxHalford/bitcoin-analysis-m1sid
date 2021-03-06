import Quandl
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn
from datetime import datetime

fig, ax = plt.subplots()
fig2, ax2 = plt.subplots()

# Cours du bitcoin
cours = Quandl.get('BCHAIN/MKPRU', authtoken='ri21BpjKtw3SVkCYWpKw',
                   collapse='daily')
cours['Value'].plot(label='Cours', ax=ax)

# Nombre de transactions
transactions = Quandl.get('BCHAIN/NTRAN', authtoken='ri21BpjKtw3SVkCYWpKw',
                          collapse='daily')
transactions['Value'].plot(label='Transactions', ax=ax2)

# Evènements silkroad
silkroad = [
    {'nom': 'Ouverture 1.0', 'date': datetime(year=2011, month=2, day=1), 'couleur': 'm'},
    {'nom': 'Fermeture 1.0', 'date': datetime(year=2013, month=10, day=2), 'couleur': 'r'},
    {'nom': 'Ouverture 2.0', 'date': datetime(year=2013, month=11, day=6), 'couleur': 'g'},
    {'nom': 'Fermeture 2.0', 'date': datetime(year=2014, month=11, day=6), 'couleur': 'k'}
]

for evenement in silkroad:
    ax.axvline(x=evenement['date'], label=evenement['nom'], color=evenement['couleur'])
    ax2.axvline(x=evenement['date'], label=evenement['nom'], color=evenement['couleur'])

ax.legend(loc='best')
ax.set_title('Cours du bitcoin et évènements relatifs au Silk Road')
ax.set_xlabel('Date')
ax.set_ylabel('Cours')

ax2.legend(loc='best')
ax2.set_title('Nombre de transactions de bitcoins et évènements relatifs au Silk Road')
ax2.set_xlabel('Date')
ax2.set_ylabel('Transactions')

plt.show()
