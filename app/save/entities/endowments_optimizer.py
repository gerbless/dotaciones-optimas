class EendowmentsOptimizer:

    def __init__(self, taks_id: str, year:int, month:int, contracts:dict, cost:str, tcn:int, location_code:str, process_time:str, created:str):
        self.taks_id = taks_id
        self.year = year
        self.month = month
        self.contracts = contracts
        self.cost = cost
        self.tcn = tcn
        self.location_code = location_code
        self.process_time = process_time
        self.created = created
