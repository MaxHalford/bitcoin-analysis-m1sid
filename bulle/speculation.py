import Quandl
import pandas as pd

# Cours du bitcoin
cours = Quandl.get('BCHAIN/MKPRU', authtoken='ri21BpjKtw3SVkCYWpKw', collapse='daily')
# Nombre de transactions
transactions = Quandl.get('BCHAIN/NTRAN', authtoken='ri21BpjKtw3SVkCYWpKw', collapse='daily')
# Nombre de bitcoins transférés
volume = Quandl.get('BCHAIN/ETRAV', authtoken='ri21BpjKtw3SVkCYWpKw', collapse='daily')


# Jointure des trois tableaux
speculation = pd.DataFrame()
speculation['cours'] = cours['Value']
speculation['transactions'] = transactions['Value']
speculation['volume'] = volume['Value']

spearman = speculation['cours'].corr(speculation['transactions'], method='spearman')
print(spearman)
