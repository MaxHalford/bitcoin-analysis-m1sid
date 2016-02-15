import unittest
import sure
import random

import pandas as pd
import numpy as np
import tweet_time

datasets = ['common_daily', 'common_weekly']
dataframe = pd.read_csv('data/{}'.format(random.choice(datasets)))


random = random.randint(0, len(dataframe.index))


class TestsFonctionnels(unittest.TestCase):

    def test_ratio(self):
        ratio = tweet_time.compute_ratio(dataframe)
        (ratio['ratio'][random]).should.be.within(0, 1)

    def test_corr_ratio_cours(self):
        corr = tweet_time.corr_ratio_cours(dataframe, scale=1)
        print(corr)
        (corr).should.be.within(0, 1)

    def test_corr_cours_ratio(self):
        corr = tweet_time.corr_cours_ratio(dataframe, scale=1)
        (corr).should.be.within(0, 1)
