__author__ = 'Chris'

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Match(Base):
    __tablename__ = 'summoner'

    id = Column(Integer, primary_key=True)
    mapId = Column(Integer)
    creation = Column(Integer)
    duration = Column(Integer)
    mode = Column(String(250))
    type = Column(String(250))
    version = Column(String(250))
    platformId = Column(String(250))
    queueType = Column(String(250))
    region = Column(String(250))
    season = Column(String(250))