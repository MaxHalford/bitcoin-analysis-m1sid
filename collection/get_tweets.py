import bs4 as BeautifulSoup


def get_year_tweets(tweet_type, year, save=False):
    ''' Récupération des tweets d'une année suivant leur type (+/-)
        tweet_type : 'positifs'/'negatifs' (str)
        year : année (int)
        save : sauvegarde du fichier (bool)

        output : les tweets concaténés (str)
    '''
    print('{0}-{1}'.format(tweet_type, year))
    with open('../data/tweets/{0}/{1}.html'.format(tweet_type, year), 'r') as myfile:
        html = myfile.read().replace('\n', '')

    soup = BeautifulSoup.BeautifulSoup(html, "html.parser")

    divs = soup.find_all(
        'p', attrs={"class": "TweetTextSize  js-tweet-text tweet-text"})

    tweets = ''
    for div in divs:
        tweets += div.get_text()

    if save:
        with open("../data/text/{0}/{1}.txt".format(tweet_type, year), "w") as text_file:
            text_file.write(tweets)

    return tweets


def get_all_tweets(tweet_type, years, save=False):
    ''' Récupération de tous les tweets d'une période suivant leur type (+/-)
        tweet_type : 'positifs'/'negatifs' (str)
        year : liste d'années (list)
        save : sauvegarde du fichier (bool)

        output : les tweets concaténés (str)
    '''

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

    if save:
        with open("../data/text/{0}/allTweets.txt".format(tweet_type), "w") as text_file:
            text_file.write(tweets)

    return tweets


# On effectue un wordcloud pour chaque année, et pour chaque sentiment
tweet_type = ['positifs', 'negatifs']
for ttype in tweet_type:
    for year in range(2010, 2016):
        tweets = get_year_tweets(ttype, year, save=True)

# On effectue un wordcloud pour les tweets positifs et un pour les tweets
# négatifs
tweet_type = ['positifs', 'negatifs']
intervalle = range(2010, 2016)
for ttype in tweet_type:
    tweets = get_all_tweets(ttype, intervalle, save=True)
