
from app.connect import connection, mymetadata_generate_process 
from app.scheduling.entities.control_of_process_endowments import EcontrolOfProcessEndowments
from sqlalchemy import Table,Integer, Column, Integer, String, DateTime, Boolean, func, Sequence
from sqlalchemy.sql import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import mapper
from app.exceptions import InvalidControlOfProcessEndowmentsException

controlOfProcessEndowments = Table('control_of_process_endowments', mymetadata_generate_process,
            Column('id_control_of_process', Integer, Sequence('control_of_process_seq'), primary_key=True, nullable=False),
            Column('id_location',Integer, nullable=False),
            Column('scheduling',DateTime, nullable=False),
            Column('attempts',Integer, nullable=False),
            Column('execution_process',Boolean, nullable=False),
            Column('monthyear',Integer, nullable=False),
            Column('activity',Integer, nullable=False),
            Column('created',DateTime, nullable=False),
            Column('updated',DateTime)
        )

mapper(EcontrolOfProcessEndowments, controlOfProcessEndowments)


def get_num_control_of_process_endowments_for_month(monthyear: int):
    return connection.session.query(func.count(EcontrolOfProcessEndowments.monthyear)).\
        filter(EcontrolOfProcessEndowments.monthyear == monthyear).scalar()

def add_control_of_process_endowments_for_month(data: EcontrolOfProcessEndowments):
    try:
        connection.session.add(data)
        connection.session.commit()
    except IntegrityError as err:
        connection.session.rollback()
        raise InvalidControlOfProcessEndowmentsException(message_user='error crear agendamiento',err_debug=str(err))

def get_exists_filter(monthyear: int, id_location: int):
    return connection.session.query(func.count(EcontrolOfProcessEndowments.monthyear)).\
        filter(EcontrolOfProcessEndowments.monthyear == monthyear, EcontrolOfProcessEndowments.id_location==id_location).scalar()

def get_select_schedules(monthyear: int, scheduling: str, config_attempts: int):
    sql = connection.session.query(EcontrolOfProcessEndowments).\
        filter(EcontrolOfProcessEndowments.execution_process == False,EcontrolOfProcessEndowments.attempts < config_attempts, EcontrolOfProcessEndowments.scheduling == scheduling, EcontrolOfProcessEndowments.monthyear == monthyear).\
            limit(1)
    return connection.session.execute(sql)

def get_activity_schedules(monthyear: int):
    return  connection.session.query(func.count(EcontrolOfProcessEndowments.monthyear)).\
        filter(EcontrolOfProcessEndowments.monthyear == monthyear, EcontrolOfProcessEndowments.activity == 2).scalar()

def update_activity_pross(idx: int, data: dict):
    try:
        connection.session.query(EcontrolOfProcessEndowments).\
            filter(EcontrolOfProcessEndowments.id_control_of_process == idx).\
            update(data,synchronize_session=False)
        connection.session.commit()
    except IntegrityError as err:
        connection.session.rollback()
        raise InvalidControlOfProcessEndowmentsException(message_user='Ocurrio un al actualizar el estado de ejecución de un agendamiento',err_debug=str(err))
