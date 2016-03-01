import unittest
import sure
import random

import pandas as pd
import numpy as np
from tweet_analysis import tweet_time
from datawarehouse import get_data

datasets = ['common_daily', 'common_weekly']
dataframe = pd.read_csv('data/{}.csv'.format(random.choice(datasets)))

equalList = [3.14] * 5
notEqualList = [3.14, 0, 3.14, 0, 0]

emptyList = [0] * 7
notEmptyList = [3.14] * 7

tweet_type = ['positifs', 'negatifs']
annees = range(2010, 2016)
realPath = 'data/tweets/{0}/{1}.html'.format(
    random.choice(tweet_type), random.choice(annees))
wrongPath = 'fake/path/{0}/{1}.html'.format(
    random.choice(tweet_type), random.choice(annees))

randomInt = random.randint(0, len(dataframe.index))


class TestsFonctionnels(unittest.TestCase):

    def test_ratio(self):
        ratio = tweet_time.compute_ratio(dataframe)
        (ratio['ratio'][randomInt]).should.be.within(0, 1)

    def test_corr_ratio_cours(self):
        corr = tweet_time.corr_ratio_cours(dataframe, scale=1)
        print(corr)
        (corr).should.be.within(0, 1)

    def test_corr_cours_ratio(self):
        corr = tweet_time.corr_cours_ratio(dataframe, scale=1)
        (corr).should.be.within(0, 1)

    def test_items_equality(self):
        equal = get_data.items_equal(equalList)
        (equal).should.be.equal(True)
        notEqual = get_data.items_equal(notEqualList)
        (notEqual).should.be.equal(False)

    def test_empty_list(self):
        empty = get_data.empty_list(emptyList)
        (empty).should.be.equal(True)
        notEmpty = get_data.empty_list(notEmptyList)
        (notEmpty).should.be.equal(False)

    def test_existing_path(self):
        real = get_data.existing_path(realPath)
        (real).should.be.equal(True)
        print(wrongPath)
        wrong = get_data.existing_path(wrongPath)
        (wrong).should.be.equal(False)
