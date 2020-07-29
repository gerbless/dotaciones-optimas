from app.connect import connection, mymetadata
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Table,Integer, Column, Integer, String, Sequence, DateTime,Boolean
from sqlalchemy.orm import mapper
from app.generate.entities.daily_constraints import EdailyConstraints

daily_constraints = Table('daily_constraints', mymetadata,
    Column('id_daily_constraints', Integer, primary_key=True, nullable=False),
    Column('day_id', Integer, nullable=False),
    Column('type', String, nullable=False),
    Column('name_contracts', String, nullable=False),
)

mapper(EdailyConstraints,daily_constraints)

def get_daily_constraints_all():
    return connection.session.query(daily_constraints).all()