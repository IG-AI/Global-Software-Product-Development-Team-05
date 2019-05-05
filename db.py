from datetime import datetime

from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from model.base import Base

engine = create_engine(SQLALCHEMY_DATABASE_URI)

Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)