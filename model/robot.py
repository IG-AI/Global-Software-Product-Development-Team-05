from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, join, select
from model.base import Base
#from models.job import Job


class Robot(Base):
    __tablename__ = 'robot'

    robot_id = Column(Integer, primary_key=True)
    role = Column(Boolean)
    current_location_x = Column(Integer)
    current_location_y = Column(Integer)
    current_direction = Column(String(20))
    #jobs = db.relationship('Job', backref='robot', lazy='dynamic')

    def __init__(self, id, role, current_location_x, current_location_y, current_direction):
        self.robot_id = id
        self.role = role
        self.current_location_x = current_location_x
        self.current_location_y = current_location_y
        self.current_direction = current_direction

    @property
    def serialize(self):
        return {
            'robot_id': self.robot_id,
            'current_location_x': self.current_location_x,
            'current_location_y': self.current_location_y,
            'current_direction': self.current_direction
        }

    def assign_coordinate(self, current_location_x, current_location_y, current_direction):
        self.current_location_x = current_location_x
        self.current_location_y = current_location_y
        self.current_direction = current_direction

    def move(self, direction):
        if (direction == "north"):
            self.current_location_y += 1
        elif (direction == "east"):
            self.current_location_x += 1
        elif (direction == "south"):
            self.current_location_y -= 1
        elif (direction == "west"):
            self.current_location_x -= 1
        elif (direction == "center"):
            {} 
        else:
            return 1

    @classmethod
    def find_by_id(cls, robot_id):
        packet = cls.query().filter_by(cls.robot_id == robot_id).first()
        return packet
