from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base
from config import Config

_engine = None
_Session = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(Config.DB_URL, echo=False, future=True)
    return _engine

def get_session():
    global _Session
    if _Session is None:
        _Session = scoped_session(sessionmaker(bind=get_engine()))
    return _Session()

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
