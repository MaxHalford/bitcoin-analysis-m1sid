import bs4 as BeautifulSoup
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from scipy.misc import imread


def read_year_tweets(tweet_type, year):
    print('{0}-{1}'.format(tweet_type, year))
    with open('../data/tweets/{0}/{1}.html'.format(tweet_type, year), 'r') as myfile:
        html = myfile.read().replace('\n', '')

    soup = BeautifulSoup.BeautifulSoup(html, "html.parser")

    divs = soup.find_all(
        'p', attrs={"class": "TweetTextSize  js-tweet-text tweet-text"})

    tweets = ''
    for div in divs:
        tweets += div.get_text()

    return tweets


def read_all_tweets(tweet_type, years):

    html = ''
    for year in years:
        print('{0}-{1}'.format(tweet_type, year))
        with open('../data/tweets/{0}/{1}.html'.format(tweet_type, year), 'r') as myfile:
            html += myfile.read().replace('\n', '')

    soup = BeautifulSoup.BeautifulSoup(html, "html.parser")

    divs = soup.find_all(
        'p', attrs={"class": "TweetTextSize  js-tweet-text tweet-text"})

    tweets = ''
    for div in divs:
        tweets += div.get_text()

    return tweets


def clean_tweets(tweets):
    print('Cleaning tweets')
    no_urls_no_tags = " ".join([word for word in tweets.split()
                                if 'http' not in word
                                and '@' not in word
                                and not word.startswith('@')
                                and word != 'RT'
                                ])
    return no_urls_no_tags


def wordcloud(data, tweet_type, year, mask='twitter_mask.png', width=1800, height=1400, dpi=300, stopwords=STOPWORDS, save=True):
    twitter_mask = imread(mask, flatten=True)
    print('Compute WordCloud')
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


# On effectue un wordcloud pour chaque année, et pour chaque sentiment
# tweet_type = ['positifs', 'negatifs']
# for ttype in tweet_type:
#     for year in range(2013, 2014):
#         tweets = read_year_tweets(ttype, year)
#         ctweets = clean_tweets(tweets)
#         wordcloud(data=ctweets, tweet_type=ttype, year=year, save=True)

# On effectue un wordcloud pour les tweets positifs et un pour les tweets
# négatifs
tweet_type = ['positifs', 'negatifs']
intervalle = range(2010, 2016)
for ttype in tweet_type:
    tweets = read_all_tweets(ttype, intervalle)
    ctweets = clean_tweets(tweets)
    wordcloud(data=ctweets, tweet_type=ttype, year='2010-2015', save=True)

# Wordcloud pour un type et une année
# tweets = read_year_tweets('negatifs', 2010)
# ctweets = clean_tweets(tweets)
# wordcloud(data=ctweets, tweet_type='negatifs', year=2010, save=True)
