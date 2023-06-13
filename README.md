# lab_controller 

### Overview

Software meant to be hosted in a Raspberry Pi 

TODO: 
- Pi config settings and setup instructions go here
- How to name Serial ports so they can be used in python script


Runs a FastAPI webserver that listens for incoming webrequests from Room Management software in order to return either puzzle status or trigger an event on the puzzle itself.

Each puzzle has its own python script (and folder for now) that will connect to the Arduinos via Serial connection (usually via USB > Ethernet > USB adapter)

TODO
- consolidate shared python (crud.py, config.py, database.py, models.py, schemas.py)

## lab_controller 

### Overview

Main controller software that runs a FastAPI webserver.

TODO
- come up with a cleaner way to handle puzzle result respone text - puzzlehelper.py
- come up with a cleaner way to resolve incoming trigger requests - crud.py

## retina_puzzle

### Overview

Manages the retina scanner puzzle

## knob_puzzle

### Overview

Manages the knob puzzle