from app.connect import connection, mymetadata
from sqlalchemy import Table,Integer, Column, Integer, String
from sqlalchemy.sql import select
from sqlalchemy.orm import mapper
from app.generate.entities.endowments import Eendowments

endowments = Table('endowments', mymetadata,
        Column('idx', Integer , primary_key=True),
        Column('store', Integer),
        Column('code', String),
        Column('working_days_week_quantity', Integer),
        Column('working_hours_week_quantity', Integer),
        Column('contracts_types', String),
        Column('name_register', String),
        Column('hrs_sem', String),
        Column('quantity', Integer)
    )

mapper(Eendowments, endowments)

def get_endowments(store:int):
    sql = connection.session.query(Eendowments).\
        filter(Eendowments.store == store)
    return connection.session.execute(sql)
    #select([endowments]).where(endowments.store == store)
    #return connection.session.execute(sql)
    #connection.session.query(Eendowments).\
    #    filter(Eendowments.store==store)
    #return connection.session.query(endowments).all()