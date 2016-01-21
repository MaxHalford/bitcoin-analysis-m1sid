import Quandl
import seaborn
import matplotlib.pyplot as plt

transactions = Quandl.get('BCHAIN/NTRAN', authtoken='ri21BpjKtw3SVkCYWpKw',
                          collapse='weekly')

transactions.plot()
plt.show()
