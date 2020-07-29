from app.connect import connection, mymetadata_generate_process
from sqlalchemy import Table,Integer, Column, Integer, String, Sequence, DateTime, ForeignKey, Boolean, ForeignKey
from sqlalchemy.sql import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import mapper, relationship
from app.generate.entities.last_month import ElastMonth
from app.input.entities.input import Einput
from app.scheduling.entities.control_of_process_endowments import EcontrolOfProcessEndowments


lastMonth = Table('last_month', mymetadata_generate_process,
        Column('id_last_month', Integer, Sequence('last_month_seq'), primary_key=True, nullable=False),
        Column('id_control_of_process_endowments',Integer,ForeignKey('control_of_process_endowments.id_control_of_process'), nullable=False),
        Column('date_month_start',DateTime, nullable=False),
        Column('date_month_end',DateTime, nullable=False),
        Column('count_month',Integer, nullable=False),
        Column('code',String, nullable=False),
        Column('recover',Boolean, nullable=False),
        Column('created',DateTime, nullable=False),
    )

mapper(ElastMonth, lastMonth, properties ={
    'input': relationship(Einput, backref='lastMonth', uselist=False),
    'control_process': relationship(EcontrolOfProcessEndowments, backref='lastMonth')
})

def get_last_month_by_code(code: str):
    return connection.session.query(ElastMonth).\
       filter(ElastMonth.code == code).\
           order_by(ElastMonth.created.desc()).\
               first()

def add_last_month(data: ElastMonth):
    try:
        connection.session.add(data)
        #connection.session.commit()
    except IntegrityError as err:
        raise err
        #connection.session.rollback()

def get_last_month_by_date(start: str, end: str, code: str):
    return connection.session.query(ElastMonth).\
       filter(ElastMonth.date_month_start == start, ElastMonth.date_month_end == end, ElastMonth.code == code).\
           order_by(ElastMonth.created).\
               first()

def delete_last_month_by_date(start: str, end: str, code: str):
    return connection.session.query(ElastMonth).\
        filter(ElastMonth.date_month_start == start, ElastMonth.date_month_end == end, ElastMonth.code == code).\
            delete()

def get_recover():
    return connection.session.query(ElastMonth).\
       filter(ElastMonth.recover == True).\
            first()

def update_last_month(idx: int, data: dict):
    try:
        connection.session.query(ElastMonth).\
            filter(ElastMonth.id_last_month == idx).\
            update(data,synchronize_session=False)
        connection.session.commit()
    except IntegrityError as err:
        connection.session.rollback()
        raise ValueError ('Error en update_recover')