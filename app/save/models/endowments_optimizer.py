
from app.connect import connection_transactions, mymetadata
from app.save.entities.endowments_optimizer import EendowmentsOptimizer
from app.generate.entities.endowments_optimization_contracts import EendowmentsOptimizationContracts
from app.save.entities.endowments_optimizer_contract_result import EendowmentsOptimizerContractResult
from sqlalchemy import Table,Integer, Column, Integer, String, DateTime, Boolean, func, Sequence, JSON, Float
from app.save.models.endowments_optimizer_contract_result import add_transactions_endowments_optimizer_contract_result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import mapper
from sqlalchemy.sql import *
from app.helpers.util import fn_now_ff_hh

endowments_optimizer = Table('endowments_optimizer', mymetadata,
    Column('id_endowments',Integer, Sequence('endowments_optimizer_seq'), primary_key=True, nullable=False),
    Column('taks_id',String, nullable=False),
    Column('year',Integer, nullable=False),
    Column('month',Integer, nullable=False),
    Column('contracts',JSON, nullable=False),
    Column('cost',String, nullable=False),
    Column('tcn',Integer, nullable=False),
    Column('location_code',String, nullable=False),
    Column('process_time',String, nullable=False),
    Column('created',DateTime, nullable=False)
)

mapper(EendowmentsOptimizer, endowments_optimizer)

def get_last_id():
    return connection_transactions.session_transactions.query(EendowmentsOptimizer).\
           order_by(EendowmentsOptimizer.created.desc()).\
               first()

def add_endowments_optimizer(endowments_optimizer: EendowmentsOptimizer, endowments_optimization_contracts: EendowmentsOptimizationContracts, contracts= dict):
    connection_transactions.session_transactions.begin()
    try:
        connection_transactions.session_transactions.add(endowments_optimizer)
        id_endowments = get_last_id().id_endowments

        for ls in endowments_optimization_contracts:
            for contract in contracts:
                if ls.name_contracts == contract:
                    res = EendowmentsOptimizerContractResult(ls.id_optimization_contracts, id_endowments,contracts[contract],fn_now_ff_hh())
                    add_transactions_endowments_optimizer_contract_result(data=res)

        connection_transactions.session_transactions.commit()
    except IntegrityError as err:
        connection_transactions.session_transactions.rollback()
        raise ValueError('err al intentar crear los datos de endowments_optimizer')