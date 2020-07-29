class EendowmentsOptimizerContractResult():
    def __init__(self, optimization_contract_id: int, endowments_id: int, value, created: str):
      self.optimization_contract_id = optimization_contract_id
      self.endowments_id = endowments_id
      self.value = value
      self.created = created
