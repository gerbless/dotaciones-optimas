from app.connect import connection, mymetadata_generate_process
from sqlalchemy import Table,Integer, Column, Integer, String, Sequence, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import mapper, relationship
from app.input.entities.input import Einput
from app.generate.entities.last_month import ElastMonth

table_inputs = Table('inputs', mymetadata_generate_process,
        Column('id_input', Integer, Sequence('inputs_endowments_seq'), primary_key=True, nullable=False),
        Column('taks_id',String, nullable=False),
        Column('input_json',JSON, nullable=False),
        Column('is_active',Boolean, nullable=False),
        Column('last_month_id',Integer, ForeignKey('last_month.id_last_month'), nullable=False),
        Column('attempts',Integer, nullable=False),
        Column('created',DateTime, nullable=False),
        Column('updated',DateTime)
    )

mapper(Einput, table_inputs, properties ={
    'last_month': relationship(ElastMonth, backref='table_inputs')
})

def add_input(data: Einput):
    try:
        connection.session.add(data)
        connection.session.commit()
    except IntegrityError as err:
        connection.session.rollback()
        raise err

def get_endowments_result():
    return connection.session.query(Einput).\
       filter(Einput.is_active == True).\
           order_by(Einput.created).\
               first()

def update_input(idx: int, data: dict):
    try:
        connection.session.query(Einput).\
            filter(Einput.id_input == idx).\
            update(data,synchronize_session=False)
        connection.session.commit()
    except IntegrityError as err:
        connection.session.rollback()
        raise ValueError ('Error al actualizar estado del input')

def delete_input(idx: int):
    #try:
        connection.session.query(Einput).\
            filter(Einput.id_input == idx).delete()
        connection.session.commit()
    #except IntegrityError as err:
    #    raise err