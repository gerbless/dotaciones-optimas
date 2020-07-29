class EcontrolOfProcessEndowments:

    def __init__(self, id_location: int, scheduling: str, attempts: int, execution_process: bool, monthyear: int,
                activity: int, created: str, updated: str):
        self.id_location = id_location
        self.scheduling = scheduling
        self.attempts = attempts
        self.execution_process = execution_process
        self.monthyear = monthyear
        self.activity = activity
        self.created = created
        self.updated = updated