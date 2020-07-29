from app.connect import connection, Base
from sqlalchemy import Integer, Column, Integer, String
from sqlalchemy.sql import select

class posts(Base):
    __tablename__ = 'post'
    local = Column(String, primary_key=True)
    tipo_caja = Column(Integer)

def get_posts(id_location: str):
    sql = select([posts]).where(posts.local == id_location)
    return connection.session.execute(sql)