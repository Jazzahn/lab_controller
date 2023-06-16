# knob_puzzle/main.py

import serial
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from utils import models, schemas, crud
from utils.database import SessionLocal, engine, SessionManager
# import utils.retina_puzzle.database
import logging
import logging.handlers as handlers

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

logger = logging.getLogger('knob_puzzle')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logHandler = handlers.RotatingFileHandler('knob.log', maxBytes=5000000, backupCount=1)
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
    with SessionManager() as db:
        if db_puzzle := crud.get_db_puzzle_by_name(db=db, puzzle_name=puzzle):
            return db_puzzle.phase
        else:
            print(f"Puzzle not initialized in database")

try:
    ser = serial.Serial('/dev/Knob', 9600, timeout=10)
    ser.reset_input_buffer
    while True:
        if ser.in_waiting > 0:
            current_phase = get_phase_status(puzzle="knob")

            # If the current phase is 99, send 99 to the Knob
            if current_phase == 99:
                ser.write(b"99")
            # If the current phase is 6, send 6 to the Knob
            if current_phase == 6:
                ser.write(b"6")

            # Get the line from the Knob
            line = ser.readline().decode('utf-8').rstrip()

            # If the line starts with "Debug", log it
            if line.startswith("Debug"):
                logger.info(line)
                print(line)
            
            # If the line is the same as the current phase, update the database
            elif int(line) == current_phase:
                print(f"Same Value")
            
            # if the line is different from the current phase and isnt a debug message
            elif int(line) != current_phase and line[:1] != "D":
                print(f"New Value of {line}")
                logger.info(f"New Value of {line}")

                # Update the database with the new phase
                with knob_puzzle.database.SessionManager() as db:
                    if db_puzzle := crud.get_db_puzzle_by_name(db=db, puzzle_name="knob"):
                        crud.update_db_phase(db=db, db_puzzle=db_puzzle, new_phase=line)
                    else:
                        print(f"Couldn't update for some reason")
                        logger.info(f"Couldn't update for some reason")

                current_phase = line

            print(f"Serial: {line} | Current Phase: {current_phase}")
            logger.info(f"Serial: {line} | Current Phase: {current_phase}") 

except Exception as e:
    print(e)
    print(f"Puzzle Unplugged")
    logger.info(f"Puzzle Unplugged")
                        


            
