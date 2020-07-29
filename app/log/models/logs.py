from app.connect import connection, Base, mymetadata_generate_process 
from sqlalchemy import Table,Integer, Column, create_engine, Integer, String, DateTime, Boolean, func, Sequence
from sqlalchemy.sql import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import mapper
from app.log.entities.logs import Elogs


logs = Table('logs', mymetadata_generate_process,
            Column('id', Integer, Sequence('logs_seq'), primary_key=True, nullable=False),
            Column('id_control_of_process',Integer, nullable=False),
            Column('level',String, nullable=False),
            Column('message',String, nullable=False),
            Column('created',DateTime, nullable=False),
        )

mapper(Elogs, logs)

def add(data: Elogs):
    try:
        connection.session.add(data)
        connection.session.commit()
    except IntegrityError as err:
        connection.session.rollback()
        raise ValueError('Error al guardar un log')