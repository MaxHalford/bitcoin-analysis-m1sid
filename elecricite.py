import Quandl
import seaborn
import matplotlib.pyplot as plt

electricite = Quandl.get('FRED/CUSR0000SEHF01', collapse='weekly',
                         authtoken='ri21BpjKtw3SVkCYWpKw')

electricite.plot()
plt.show()
