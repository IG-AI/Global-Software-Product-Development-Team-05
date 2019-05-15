from db import DB
from model.base import Base
#from models.job import Job


class Address(Base):
    __tablename__ = 'address'

    id = DB.Column(DB.Integer, primary_key=True)
    host = DB.Column(DB.String(20))

    def __init__(self, id, host):
        self.id = id
        self.host = host

    @property
    def serialize(self):
        return {
            'id': self.id,
            'address': self.host
        }

    def assign_address(self, host):
        self.host = host

    @classmethod
    def find_by_id(cls, id):
        packet = cls.query.filter_by(id = id).first()
        return packet

    @classmethod
    def find_by_host(cls, host):
        packet = cls.query.filter_by(host = host).first()
        return packet
