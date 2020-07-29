from app.connect import connection, Base
from sqlalchemy import Integer, Column, Integer, String, func
from sqlalchemy.sql import select

class locations(Base):
    __tablename__ = 'locations'
    id_location = Column(Integer, primary_key=True)
    code = Column(String)
    location_mirror_code = Column(String)


def get_locations():
    s = select([locations])
    return connection.session.execute(s)

def get_num_locations():
    return connection.session.query(func.count(locations.id_location)).scalar()

def get_location_by_id(idx: int):
    return connection.session.query(locations).get(idx)