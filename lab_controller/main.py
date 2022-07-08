# lab_controller/main.py

import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine
from .config import get_settings
from .puzzlehelper import return_status_text

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def raise_not_found(request):
    message = f"Puzzle '{request.puzzle}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

def get_puzzle_info(db_puzzle: models.Puzzle) -> schemas.Puzzle:
    return db_puzzle

@app.get("/")
def get_root():
    return "This is Root"

@app.get("/status/{puzzle}")
def get_phase_status(
    puzzle: str,
    request: Request, 
    db: Session = Depends(get_db)
):
    if db_puzzle := crud.get_db_puzzle_by_name(db=db, puzzle_name=puzzle):
        phase = db_puzzle.phase
        status_text = return_status_text(puzzle=puzzle, status=phase)
        return status_text
    else:
        raise_not_found(request)

@app.get("/create/{puzzle}", response_model=schemas.Puzzle)
def create_puzzle(
    puzzle: str,
    request: Request,
    db: Session = Depends(get_db)
):
    db_puzzle = crud.create_db_puzzle(db=db, puzzle=puzzle)
    return get_puzzle_info(db_puzzle)

@app.get("/trigger/{puzzle}/{trigger}")
def trigger_puzzle(
    puzzle: str,
    trigger: str,
    request: Request,
    db: Session = Depends(get_db)
):
    puzzle_trigger = crud.trigger_db_puzzle(db=db, puzzle_name=puzzle, trigger_name=trigger)
    return puzzle_trigger