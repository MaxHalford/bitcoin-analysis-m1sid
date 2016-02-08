import Quandl
import seaborn
import matplotlib.pyplot as plt

NONCE = pow(2, 32)

difficultes = Quandl.get('BCHAIN/DIFF', authtoken='ri21BpjKtw3SVkCYWpKw',
                         collapse='daily')


def bitcoins_par_jour(difficulte, hashrate):
    '''
    Retourne le nombre de bitcoins trouvés en moyenne pour un jour.

    - difficulte: imposée par le système
    - hashrate: en hashs par seconde
    '''
    return 24 / (difficulte * NONCE / hashrate / 3600)


def cout_par_jour(consommation, prix):
    '''
    Retourne le cout en electricité.

    - consommation: consommation en kilowatt/heure
    - prix: prix du kilowatt/heure
    '''
    return 24 * consommation * prix

difficulte = 20000
hashrate = 7722000 * 1000000
watts = 3436

difficultes['bitcoins'] = bitcoins_par_jour(difficultes['Value'], hashrate)