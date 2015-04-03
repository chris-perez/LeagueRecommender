__author__ = 'Chris'

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Summoner(Base):
    __tablename__ = 'summoner'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)