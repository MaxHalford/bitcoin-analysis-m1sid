import Quandl
import pandas as pd

# Difficultés au cours du temps
difficultes = Quandl.get('BCHAIN/DIFF', authtoken='ri21BpjKtw3SVkCYWpKw',
                         collapse='daily')
# Prix de l'électricité
electricite = pd.read_csv('data/electricite.csv')
electricite.index = pd.to_datetime(electricite.periode, format='%Y_%m')
electricite.drop('periode', axis=1, inplace=True)

# Machines
machines = pd.read_csv('data/machines.csv', index_col='nom')