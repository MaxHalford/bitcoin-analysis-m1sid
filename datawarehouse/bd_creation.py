from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey

Base = declarative_base()


class Utilisateur(Base):
    __tablename__ = 'utilisateurs'

    id = Column(Integer, autoincrement=True, primary_key=True)
    nom = Column(String)


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, autoincrement=True, primary_key=True)
    contenu = Column(String)
    likes = Column(Integer)
    retweets = Column(Integer)
    sentiment = Column(String)
    utilisateur = Column(String, ForeignKey('utilisateurs.id'))
    date = Column(String, ForeignKey('dates.id'))


class Date(Base):
    __tablename__ = 'dates'

    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(DateTime)


class Terme(Base):
    __tablename__ = 'termes'

    id = Column(Integer, autoincrement=True, primary_key=True)
    terme = Column(String)


class Url(Base):
    __tablename__ = 'urls'

    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String)


class Hashtag(Base):
    __tablename__ = 'hashtags'

    id = Column(Integer, autoincrement=True, primary_key=True)
    hashtag = Column(String)


class TermeDansTweet(Base):
    __tablename__ = 'terme_dans_tweets'

    id = Column(Integer, autoincrement=True, primary_key=True)
    terme = Column(Integer, ForeignKey('termes.id'))
    tweet = Column(Integer, ForeignKey('tweets.id'))


class UrlDansTweet(Base):
    __tablename__ = 'url_dans_tweet'

    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(Integer, ForeignKey('urls.id'))
    tweet = Column(Integer, ForeignKey('tweets.id'))


class HashtagDansTweet(Base):
    __tablename__ = 'hashtag_dans_tweet'

    id = Column(Integer, autoincrement=True, primary_key=True)
    hashtag = Column(Integer, ForeignKey('hashtags.id'))
    tweet = Column(Integer, ForeignKey('tweets.id'))


engine = create_engine('sqlite:///tweets.db')
Base.metadata.create_all(engine)
