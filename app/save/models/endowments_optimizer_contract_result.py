from app.connect import connection_transactions, mymetadata
from sqlalchemy import Table,Integer, Column, Integer, String, Sequence, DateTime
from sqlalchemy.orm import mapper
from app.save.entities.endowments_optimizer_contract_result import EendowmentsOptimizerContractResult


endowments_optimizer_contract_result = Table('endowments_optimizer_contract_result', mymetadata,
    Column('id_endowments_optimizer_contract_result',Integer, Sequence('endowments_optimizer_contract_result_seq'), primary_key=True, nullable=False),
    Column('optimization_contract_id',Integer, nullable=False),
    Column('endowments_id',Integer, nullable=False),
    Column('value',Integer, nullable=False),
    Column('created',DateTime, nullable=False)
)

mapper(EendowmentsOptimizerContractResult, endowments_optimizer_contract_result)

 
def add_transactions_endowments_optimizer_contract_result(data:EendowmentsOptimizerContractResult):
    connection_transactions.session_transactions.add(data)