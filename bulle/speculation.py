import Quandl
import pandas as pd
import seaborn as sns

speculation = pd.DataFrame()

codes = {
    'Cours': 'BCHAIN/MKPRU',
    'Transactions': 'BCHAIN/NTRAN',
    'Volume en dollars': 'BCHAIN/ETRVU',
    'Volume en bitcoins': 'BCHAIN/ETRAV'
}

for indicateur, code in codes.items():
    df = Quandl.get(code, authtoken='ri21BpjKtw3SVkCYWpKw', collapse='daily')
    speculation[indicateur] = df['Value']

corr = speculation.corr(method='spearman')
sns.heatmap(corr)
