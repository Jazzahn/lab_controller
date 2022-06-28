# lab_controller/crud.py

from sqlalchemy.orm import Session
from datetime import datetime

from . import models, schemas

def create_db_puzzle(db: Session, puzzle: str) -> models.Puzzle:
    db_puzzle = models.Puzzle(
        puzzle_name=puzzle
    )
    db.add(db_puzzle)
    db.commit()
    db.refresh(db_puzzle)
    return db_puzzle

def update_db_phase(db: Session, db_puzzle: schemas.Puzzle, phase: int) -> models.Puzzle:
    db_puzzle.phase = phase
    db.commit()
    db.refresh(db_puzzle)
    return db_puzzle

def get_db_puzzle_by_name(db: Session, puzzle_name: str) -> models.Puzzle:
    return (
        db.query(models.Puzzle)
        .filter(models.Puzzle.puzzle_name == puzzle_name)
        .first()
    )