# retina_puzzle/main.py

import serial
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine
import retina_puzzle.database

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_phase_status(
    puzzle: str,
):
    with retina_puzzle.database.SessionManager() as db:
        if db_puzzle := crud.get_db_puzzle_by_name(db=db, puzzle_name=puzzle):
            return db_puzzle.phase
        else:
            print(f"Puzzle not initialized in database")

try:
    ser = serial.Serial('/dev/tty.usbserial-1430', 9600, timeout=None)
    ser.reset_input_buffer    
    
    while True:
        if ser.in_waiting > 0:
            current_phase = get_phase_status(puzzle="retina")
            if current_phase == 3:
                ser.write(b"3")
            line = ser.readline().decode('utf-8').rstrip()
            if line[:5] == "Debug":
                print(line)
            elif line == current_phase:
                print(f"Same Val")
            elif line != current_phase and line[:1] != "D":
                print(f"New Val of {line}")
                with retina_puzzle.database.SessionManager() as db:
                    if db_puzzle := crud.get_db_puzzle_by_name(db=db, puzzle_name="retina"):
                        crud.update_db_phase(db=db, db_puzzle=db_puzzle, phase=line)
                    else:
                        print(f"Couldn't update for some reason")
                current_phase = line
            

            print(f"Serial: {line} -- Current Phase: {current_phase}")
except:
    print(f"Puzzle Unplugged")

