import Quandl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

speculation = pd.DataFrame()

codes = {
    'Cours': 'BCHAIN/MKPRU',
    'Transactions': 'BCHAIN/NTRAN',
    'Volume dollars': 'BCHAIN/ETRVU',
    'Volume bitcoins': 'BCHAIN/ETRAV'
}



for indicateur, code in codes.items():
    df = Quandl.get(code, authtoken='ri21BpjKtw3SVkCYWpKw', collapse='daily')
    speculation[indicateur] = df['Value']

corr = speculation.corr(method='pearson')
sns.heatmap(corr, vmin=0, vmax=1, annot=True, cmap='YlGnBu', linewidths=.7, fmt='f')

plt.savefig('speculation_heatmap_pearson.png', dpi=200)
