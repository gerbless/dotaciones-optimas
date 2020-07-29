from app.connect import connection, mymetadata
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Table,Integer, Column, Integer, String, Sequence, DateTime,Boolean
from sqlalchemy.orm import mapper
from app.generate.entities.launch_entries import ElaunchEntries

launch_entries = Table('endowments_lunch_entries', mymetadata,
    Column('id_endowments_lunch_entries', Integer, primary_key=True, nullable=False),
    Column('title', String, nullable=False),
    Column('start', String, nullable=False),
    Column('end', String, nullable=False),
    Column('is_active', Boolean, nullable=False),
    Column('created', DateTime, nullable=False),
    Column('updated', DateTime)
)

mapper(ElaunchEntries, launch_entries)


def get_launch_entries_all():
    return connection.session.query(launch_entries).all()