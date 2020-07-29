class EendowmentsOptimizationContracts:
    def __init__(self, name_contracts: str, daily_blocks:int, weekly_work_days:int, cost_monday:int, cost_tuesday:int, cost_wednesday:int, cost_thursday:int, cost_friday:int, cost_saturday:int, cost_sunday:int, fixed_week:bool, created: str, updated:str=None):
        self.name_contracts = name_contracts
        self.daily_blocks = daily_blocks
        self.weekly_work_days = weekly_work_days
        self.cost_monday = cost_monday
        self.cost_tuesday = cost_tuesday
        self.cost_wednesday = cost_wednesday
        self.cost_thursday = cost_thursday
        self.cost_friday = cost_friday
        self.cost_saturday = cost_saturday
        self.cost_sunday = cost_sunday
        self.fixed_week = fixed_week
        self.created = created
        self.updated = updated
