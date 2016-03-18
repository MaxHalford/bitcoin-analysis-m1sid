import pandas as pd
import seaborn
from bd_creation import engine
import matplotlib.pyplot as plt

# Code de vrai salaud

elec = pd.read_sql_query('''
SELECT *
FROM electricites
''', engine)
elec.rename(columns={'date': 'date_elec'}, inplace=True)

mac = pd.read_sql_query('''
SELECT *
FROM machines
''', engine)

diff = pd.read_sql_query('''
SELECT *
FROM difficultes
''', engine)
diff.rename(columns={'date': 'date_diff', 'valeur': 'valeur_diff'}, inplace=True)

bit = pd.read_sql_query('''
SELECT *
FROM bitcoins
''', engine)
bit.rename(columns={'date': 'date_bit', 'valeur': 'valeur_bit'}, inplace=True)


year_month = lambda date: '{0}-{1}'.format(date.year, date.month)

elec['date_elec'] = pd.to_datetime(elec['date_elec']).apply(year_month)
bit_diff = pd.merge(diff, bit, left_on='date_diff', right_on='date_bit')
bit_diff['date_diff'] = pd.to_datetime(bit_diff['date_diff']).apply(year_month)
bde = pd.merge(bit_diff, elec, left_on='date_diff', right_on='date_elec')

# Propre
data = bde[['valeur_diff', 'date_bit', 'valeur_bit', 'prix']]
data.rename(columns={
    'valeur_diff': 'difficulte',
    'date_bit': 'date',
    'valeur_bit': 'valeur',
    
}, inplace=True)
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)


NONCE = pow(2, 32)

# Nombre de bitcoins trouvés en moyenne pour un jour
bitcoins_par_jour = lambda h, d: (675 * h) / (33554432 * (d+1))
gain = lambda h, d, c: bitcoins_par_jour(h * 1000000, d) * c
# Coût en électricité par jour
cout = lambda k, e: 24 * k * e


hashrate = 441000.0
consommation = 382.0


data['gain'] = [
    gain(hashrate, r['difficulte'], r['valeur'])
    for i, r in data.iterrows()
]

data['cout'] = [
    cout(consommation, r['prix'])
    for i, r in data.iterrows()
]

data['profit'] = data['gain'] - data['cout']

fig, ax = plt.subplots()
data['gain'].plot(ax=ax, label='Gain')
data['cout'].plot(ax=ax, label='Coût')
data['profit'].plot(ax=ax, label='Profit')
ax.set_xlabel('Date')
ax.set_ylabel('Dollars')
ax.legend(loc='best')

plt.savefig('profit2.png', dpi=400)
