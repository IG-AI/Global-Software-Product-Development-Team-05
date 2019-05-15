from db import DB
from model.base import Base
#from models.job import Job

class Account(Base):
    __tablename__ = 'account'

    id = DB.Column(DB.Integer, primary_key=True)
    role = DB.Column(DB.Boolean)
    username = DB.Column(DB.String(20))
    password = DB.Column(DB.String(20))
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
            'id': self.id,
            'role': self.role,
            'username': self.username,
            'password': self.password           
        }

    @classmethod
    def find_by_id(cls, id):
        packet = cls.query.filter_by(id = id).first()
        return packet

    @classmethod
    def find(cls, username, password):
        packet = cls.query.filter_by(username = username, password = password).first()
        return packet

    @classmethod
    def find_by_name(cls, username):
        packet = cls.query.filter_by(username = username).first()
        return packet
