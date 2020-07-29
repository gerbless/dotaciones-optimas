from app.connect import connection, mymetadata_generate_process
from sqlalchemy import Table,Integer, Column, Integer, String, Sequence, DateTime, Boolean, JSON, Text, ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import mapper, relationship
from app.input.entities.result_input import Eresult_input
from app.input.entities.input import Einput

table_result_input = Table('result_input', mymetadata_generate_process,
        Column('id_taks', String, primary_key=True, nullable=False),
        Column('input_id',Integer, ForeignKey('inputs.id_input'), nullable=False),
        Column('state',String, nullable=False),
        Column('types',String),
        Column('message',String),
        Column('traceback',Text),
        Column('result',JSON, nullable=False),
        Column('created',DateTime, nullable=False)
    )

mapper(Eresult_input, table_result_input, properties ={
    'input': relationship(Einput, backref='table_result_input', order_by=table_result_input.c.id_taks)
})

def add_result_input(data: Eresult_input):
    try:
        connection.session.add(data)
        connection.session.commit()
    except IntegrityError as err:
        connection.session.rollback()
        raise err

def delete_result_input(id_input: str):
    #try:
        connection.session.query(Eresult_input).\
            filter(Eresult_input.input_id == id_input).delete()
        connection.session.commit()
    #except IntegrityError as err:
    #    raise err

def get_error_result():
     return connection.session.query(Eresult_input).\
        filter(Eresult_input.state == 'ERROR-INPUT').all()