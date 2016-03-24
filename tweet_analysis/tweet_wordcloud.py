from wordcloud import WordCloud, STOPWORDS
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy.misc import imread
import os.path


def read_year_tweets(tweet_type, year):
    ''' Lecture des tweets pour un type et une année donnée
        tweet_type : classification du tweet (+/-) (str)
        year : année (int)

        content : tweets (str)
    '''
    fname = "../data/text/{0}/{1}.txt".format(tweet_type, year)
    if os.path.isfile(fname):
        with open(fname, 'r') as content_file:
            content = content_file.read()
        return content
    else:
        raise ValueError(
            "Pas de tweets {0} - {1} trouvés".format(tweet_type, year))


def clean_tweets(tweets):
    ''' Nettoyage des tweets
        tweets : tweets brut (str)

        no_urls_no_tags : tweets nettoyés (str)
    '''
    no_urls_no_tags = " ".join([word for word in tweets.split()
                                if 'http' not in word
                                and '@' not in word
                                and not word.startswith('@')
                                and word != 'RT'
                                ])
    return no_urls_no_tags


def wordcloud(data, tweet_type, year, mask='twitter_mask.png', width=1800, height=1400, dpi=300, stopwords=STOPWORDS, save=True):
    twitter_mask = imread(mask, flatten=True)
    more_stopwords = {'oh', 'will', 'hey', 'yet'}
    STOPWORDS = stopwords.union(more_stopwords)

    wordcloud = WordCloud(
        font_path='quartzo.ttf',
        stopwords=stopwords,
        background_color='white',
        width=width,
        height=height,
        mask=twitter_mask
    ).generate(data)

    plt.imshow(wordcloud)
    plt.axis('off')

    if save:
        plt.savefig(
            'wordclouds/wordcloud_{0}_{1}.png'.format(tweet_type, year), dpi=dpi)
    plt.show()


tweet_type = ['positifs', 'negatifs']
for ttype in tweet_type:
    for year in range(2010, 2016):
        tweets = read_year_tweets(ttype, year)
        ctweets = clean_tweets(tweets)
        wordcloud(data=ctweets, tweet_type=ttype, year=year, save=False)
