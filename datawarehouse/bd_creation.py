from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, Float, String ForeignKey

Base = declarative_base()


class Utilisateur(Base):
    __tablename__ = 'utilisateurs'

    id = Column(Integer, autoincrement=True, primary_key=True))
    nom = Column(String)


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, autoincrement=True, primary_key=True))
    contenu = Column(String)
    utilisateur = Column(String, db.ForeignKey('utilisateurs.id'))
    date = Column(String, db.ForeignKey('dates.id'))


class Date(Base):
    __tablename__ = 'dates'

    id = Column(Integer, autoincrement=True, primary_key=True))
    date = Column(Datetime)


class Terme(Base):
    __tablename__ = 'termes'

    id = Column(Integer, autoincrement=True, primary_key=True))
    terme = Column(String)


class Url(Base):
    __tablename__ = 'urls'

    id = Column(Integer, autoincrement=True, primary_key=True))
    url = Column(String)


class Hashtag(Base):
    __tablename__ = 'urls'

    id = Column(Integer, autoincrement=True, primary_key=True))
    hashtag = Column(String)


class TermeDansTweet(Base):
    __tablename__ = 'terme_dans_tweets'

    id = Column(Integer, autoincrement=True, primary_key=True))
    terme = Column(Integer, db.ForeignKey('termes.id'))
    tweet = Column(Integer, db.ForeignKey('tweets.id'))


class UrlDansTweet(Base):
    __tablename__ = 'url_dans_tweet'

    id = Column(Integer, autoincrement=True, primary_key=True))
    url = Column(Integer, db.ForeignKey('urls.id'))
    tweet = Column(Integer, db.ForeignKey('tweets.id'))


class HashtagDansTweet(Base):
    __tablename__ = 'hashtag_dans_tweet'

    id = Column(Integer, autoincrement=True, primary_key=True))
    hashtag = Column(Integer, db.ForeignKey('hashtags.id'))
    tweet = Column(Integer, db.ForeignKey('tweets.id'))


engine = create_engine('sqlite:///tweets.db')
Base.metadata.create_all(engine)
