import db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db import session_scope as s

#Base = declarative_base()

class Base():
    __abstract__ = True

    def save_to_db(self):
        s.add(self)
        s.commit()

    def delete_from_db(self):
        s.delete(self)
        s.commit()

    @classmethod
    def query(cls):
        return s.query(cls)

        #def filter_by(*kwargs):
            #kwargskwargskwargss.query(cls).filter_by(*kwargs)
