__author__ = 'Chris'

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Summoner(Base):
    __tablename__ = 'summoner'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    profileIconId = Column(Integer)
    revisionDate = Column(Integer)
    summonerLevel = Column(Integer)



# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine("data.db")

# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)