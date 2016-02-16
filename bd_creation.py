from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, DateTime, Integer, Float, String,
                        PrimaryKeyConstraint)

Base = declarative_base()


class Difficulte(Base):
    __tablename__ = 'difficultes'

    date = Column(DateTime, primary_key=True)
    valeur = Column(Integer)


class Electricite(Base):
    __tablename__ = 'electricites'

    date = Column(DateTime)
    pays = Column(String)
    prix = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint('date', 'pays', name='pk_electricites'),
    )


class Machine(Base):
    __tablename__ = 'machines'

    nom = Column(String, primary_key=True)
    hashrate = Column(Integer)
    consommation = Column(Float)
    cout = Column(Float)


class Bitcoin(Base):
    __tablename__ = 'bitcoins'

    date = Column(DateTime, primary_key=True)
    valeur = Column(Float)


engine = create_engine('sqlite:///bitcoin_profit.db')
Base.metadata.create_all(engine)
