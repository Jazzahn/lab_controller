# retina_puzzle/main.py

import serial
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine
import retina_puzzle.database
import logging
import logging.handlers as handlers

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

logger = logging.getLogger('retina_puzzle')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logHandler = handlers.RotatingFileHandler('retina.log', maxBytes=5000000, backupCount=1)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)

logger.addHandler(logHandler)

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
    ser = serial.Serial('/dev/Retina', 9600, timeout=10)
    ser.reset_input_buffer
    while True:
        if ser.in_waiting > 0:
            current_phase = get_phase_status(puzzle="retina")

            # If the current phase is 6, send 6 to the Retina
            if current_phase == 6:
                ser.write(b"6")
            # If the current phase is 3, send 3 to the Retina
            if current_phase == 3:
                ser.write(b"3")

            # Get the line from the Retina
            line = ser.readline().decode('utf-8').rstrip()

            # If the line starts with "Debug", log it
            if line[:5] == "Debug":
                print(line)
                logger.info(line)

            # If the line is the same as the current phase, log it
            elif int(line) == current_phase:
                print(f"Same Val")

            # If the line is different from the current phase and isn't a debug message
            elif int(line) != current_phase and line[:1] != "D":
                print(f"New Val of {line}")
                logger.info(f"New Value of {line}")

                # Update the database with the new phase
                with retina_puzzle.database.SessionManager() as db:
                    if db_puzzle := crud.get_db_puzzle_by_name(db=db, puzzle_name="retina"):
                        crud.update_db_phase(db=db, db_puzzle=db_puzzle, phase=line)
                    else:
                        print(f"Couldn't update for some reason")
                        logger.warning("Couldn't update for some Reason")

                current_phase = line

            print(f"Serial: {line} -- Current Phase: {current_phase}")
            logger.info(f"Serial: {line} -- Current Phase: {current_phase}")
except Exception as e:
    print(e)
    print(f"Puzzle Unplugged")
    logger.warning("Puzzle Not Available")

