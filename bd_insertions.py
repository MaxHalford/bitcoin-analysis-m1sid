import Quandl
import pandas as pd
from sqlalchemy.orm import sessionmaker
from bd_creation import engine
from bd_creation import Base, Difficulte, Electricite, Machine, Bitcoin

Base.metadata.bind = engine
session = sessionmaker(bind=engine)()

# Difficultés au cours du temps
session.query(Difficulte).delete()
difficultes = Quandl.get('BCHAIN/DIFF', authtoken='ri21BpjKtw3SVkCYWpKw',
                         collapse='daily')
difficultes['date'] = difficultes.index
difficultes.apply(lambda x: session.add(Difficulte(date=x['date'],
                                                   valeur=x['Value'])), axis=1)
session.commit()

# A finir...

# Prix de l'électricité
electricite = pd.read_csv('data/electricite.csv')
electricite.index = pd.to_datetime(electricite.periode, format='%Y_%m')
electricite.drop('periode', axis=1, inplace=True)

# Machines
machines = pd.read_csv('data/machines.csv', index_col='nom')
