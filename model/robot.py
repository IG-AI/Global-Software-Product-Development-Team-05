from db import DB
from model.base import Base
#from models.job import Job


class Robot(Base):
    __tablename__ = 'robot'

    id = DB.Column(DB.Integer, primary_key=True)
    role = DB.Column(DB.Boolean)
    current_location_x = DB.Column(DB.Integer)
    current_location_y = DB.Column(DB.Integer)
    current_direction = DB.Column(DB.String(20))

    def __init__(self, id, role, current_location_x, current_location_y, current_direction):
        self.id = id
        self.role = role
        self.current_location_x = current_location_x
        self.current_location_y = current_location_y
        self.current_direction = current_direction

    @property
    def serialize(self):
        return {
            'id': self.id,
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
    def find_by_id(cls, id):
        packet = cls.query.filter_by(id = id).first()
        return packet
