# retina_puzzle/schemas.py

from datetime import datetime
from pydantic import BaseModel

class PuzzleBase(BaseModel):
    puzzle_name: str

class Puzzle(PuzzleBase):
    phase: int
    last_update: datetime

    class Config:
        orm_mode = True