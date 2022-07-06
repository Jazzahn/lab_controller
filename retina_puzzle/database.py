# retina_puzzle/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import warnings

from .config import get_settings

engine = create_engine(
    get_settings().db_url, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
Base = declarative_base()

@contextmanager
def SessionManager():
    db = SessionLocal()
    try:
        yield db
    except:
        # if we fail somehow rollback the connection
        warnings.warn("We somehow failed in a DB operation and auto-rollbacking...")
        db.rollback()
        raise
    finally:
        db.close()