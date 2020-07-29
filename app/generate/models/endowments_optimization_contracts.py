from app.connect import connection, mymetadata
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Table,Integer, Column, Integer, String, Sequence, DateTime,Boolean
from sqlalchemy.orm import mapper
from app.generate.entities.endowments_optimization_contracts import EendowmentsOptimizationContracts

endowmentsOptimizationContracts = Table('endowments_optimization_contracts', mymetadata,
        Column('id_optimization_contracts', Integer, primary_key=True, nullable=False),
        Column('name_contracts',Integer, nullable=False),
        Column('daily_blocks',String, nullable=False),
        Column('weekly_work_days',Integer, nullable=False),
        Column('cost_monday',Integer, nullable=False),
        Column('cost_tuesday',Integer, nullable=False),
        Column('cost_wednesday',Integer, nullable=False),
        Column('cost_thursday',Integer, nullable=False),
        Column('cost_friday',Integer, nullable=False),
        Column('cost_saturday',Integer, nullable=False),
        Column('cost_sunday',Integer, nullable=False),
        Column('fixed_week',Boolean, nullable=False),
        Column('contract',Integer, nullable=False),
        Column('permanent',Integer, nullable=False),
        Column('created', DateTime, nullable=False),
        Column('updated', DateTime),
    )

mapper(EendowmentsOptimizationContracts, endowmentsOptimizationContracts)

def get_endowments_optimization_contracts_all():
    return connection.session.query(endowmentsOptimizationContracts).all()