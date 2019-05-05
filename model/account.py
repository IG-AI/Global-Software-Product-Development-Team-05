from sqlalchemy import Column, Integer, String, Date, Boolean
from model.base import Base
#from models.job import Job

class Account(Base):
    __tablename__ = 'robot'

    account_id = Column(Integer, primary_key=True)
    role = Column(Boolean)
    username = Column(String(20))
    password = Column(String(20))
    #current_direction = db.Column(db.String(20))
    #jobs = db.relationship('Job', backref='robot', lazy='dynamic')

    def __init__(self, role, username, password):
        self.role = role
        self.username = username
        self.password = password
        #self.current_direction = current_direction

    @property
    def serialize(self):
        return {
            'account_id': self.account_id,
            'role': self.role,
            'username': self.username,
            'password': self.password           
        }

    @classmethod
    def find_by_id(cls, account_id):
        packet = cls.query().filter_by(cls.account_id == account_id).first()
        return packet
