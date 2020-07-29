from app.connect import connection, mymetadata
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Table,Integer, Column, Integer, String, Sequence, DateTime,Boolean
from sqlalchemy.orm import mapper
from app.generate.entities.job_entries import EjobEntries

job_entries = Table('job_entries', mymetadata,
    Column('location_id', Integer, primary_key=True, nullable=False),
    Column('work_days', Integer, nullable=False),
    Column('working_hours', Integer, nullable=False),
    Column('weekday', Integer, nullable=False),
    Column('hour', String, nullable=False),
)

mapper(EjobEntries,job_entries)

def get_job_entries_all():
    return connection.session.query(job_entries).all()