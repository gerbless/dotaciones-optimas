class ElastMonth:

    def __init__(self, id_control_of_process_endowments: int,
            date_month_start:str, date_month_end:str, count_month:int, code:str, created:str, recover: bool=False):

        self.id_control_of_process_endowments = id_control_of_process_endowments
        self.date_month_start = date_month_start
        self.date_month_end = date_month_end
        self.count_month = count_month
        self.code = code
        self.created = created
        self.recover = recover