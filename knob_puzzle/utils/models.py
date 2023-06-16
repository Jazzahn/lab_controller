# knob_puzzle/models.py

from tokenize import String
from sqlalchemy import DateTime, Column, Integer, String
from sqlalchemy.sql import func

from .database import Base

class Puzzle(Base):
    __tablename__ = "puzzles"

    id = Column(Integer, primary_key=True)
    puzzle_name = Column(String, unique=True, index=True)
    phase = Column(Integer, index=True, default=0)
    last_update = Column(DateTime, default=func.now(), onupdate=func.now())