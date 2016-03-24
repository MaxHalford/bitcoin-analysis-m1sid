import pandas as pd
import datetime
import re
from urllib.parse import urlparse
from sqlalchemy.orm import sessionmaker
from bd_creation import engine
from bd_creation import (Utilisateur, Tweet, Date, Terme, Url, Hashtag,
                         TermeDansTweet, UrlDansTweet, HashtagDansTweet)

session = sessionmaker(bind=engine)()
df = pd.read_csv('../data/dataframes/allTweets.csv')


# On vide les tables
session.query(Utilisateur).delete()
session.query(Tweet).delete()
session.query(Date).delete()
session.query(Terme).delete()
session.query(Url).delete()
session.query(Hashtag).delete()
session.query(TermeDansTweet).delete()
session.query(UrlDansTweet).delete()
session.query(HashtagDansTweet).delete()

for username in df['username'].unique():
    session.add(Utilisateur(nom=username))
session.commit()

for ts in df['timestamp'].unique():
    session.add(Date(date=datetime.datetime.fromtimestamp(ts / 1000)))
session.commit()

T = []
H = []
U = []


punctuation = ['!', '?', ';', ':', ',', '.']


def rm_punctuation(s):
    cleaned = "".join(l for l in s if l not in punctuation)
    print("Ligne insérée.")
    return cleaned


def get_info_from_tweet(tweet):
    hashtags = set()
    urls = set()
    termes = set()
    for elem in re.split('\s', tweet):
        # Hashtag
        if elem.startswith('#'):
            hashtags.add(rm_punctuation(elem))
        # Lien
        elif elem.startswith('http'):
            host = urlparse(elem).hostname
            urls.add(host)
        # Terme
        else:
            termes.add(rm_punctuation(elem))
    return (termes, hashtags, urls)


def add(row):
    date = datetime.datetime.fromtimestamp(row['timestamp'] / 1000)
    tweet = Tweet(
        contenu=row['tweet'],
        likes=row['likes'],
        retweets=row['retweets'],
        sentiment=row['sentiment'],
        utilisateur=row['username'],
        date=date
    )
    session.add(tweet)
    session.commit()
    tweet_id = tweet.id
    termes, hashtags, urls = get_info_from_tweet(tweet.contenu)
    for terme in termes:
        if terme not in T:
            session.add(Terme(terme=terme))
            session.commit()
            T.append(terme)
        terme_id = session.query(Terme).filter(Terme.terme == terme).one()
        session.add(TermeDansTweet(tweet=tweet_id,
                                   terme=terme_id.id))
        session.commit()
    for hashtag in hashtags:
        if hashtag not in H:
            session.add(Hashtag(hashtag=hashtag))
            session.commit()
            H.append(hashtag)
        hashtag_id = session.query(Hashtag).filter(
            Hashtag.hashtag == hashtag).one()
        session.add(HashtagDansTweet(tweet=tweet_id, hashtag=hashtag_id.id))
        session.commit()
    for url in urls:
        if url not in U:
            session.add(Url(url=url))
            session.commit()
            U.append(url)
        url_id = session.query(Url).filter(Url.url == url).one()
        session.add(UrlDansTweet(tweet=tweet_id, url=url_id.id))
        session.commit()


df.apply(lambda row: add(row), axis=1)
