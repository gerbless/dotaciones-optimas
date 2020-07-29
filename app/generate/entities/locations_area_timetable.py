class ElocationsAreaTimetable:

    def __init__(self, LOCATION_ID:int, PRE_OPEN_TIME:int, POST_CLOSE_TIME: int, START_TIME_MON:str, END_TIME_MON:str,
                START_TIME_TUE:str, END_TIME_TUE:str, START_TIME_WED:str,END_TIME_WED:str,
                START_TIME_THU:str, END_TIME_THU:str, START_TIME_FRI:str, END_TIME_FRI:str,
                START_TIME_SAT:str, END_TIME_SAT:str, START_TIME_SUN:str, END_TIME_SUN:str):

        self.LOCATION_ID = LOCATION_ID
        self.PRE_OPEN_TIME = PRE_OPEN_TIME
        self.POST_CLOSE_TIME = POST_CLOSE_TIME
        self.END_TIME_MON = END_TIME_MON
        self.START_TIME_TUE = START_TIME_TUE
        self.END_TIME_TUE = END_TIME_TUE
        self.START_TIME_WED = START_TIME_WED
        self.END_TIME_WED = END_TIME_WED
        self.START_TIME_THU = START_TIME_THU
        self.END_TIME_THU = END_TIME_THU
        self.START_TIME_FRI = START_TIME_FRI
        self.END_TIME_FRI = END_TIME_FRI
        self.START_TIME_SAT = START_TIME_SAT
        self.END_TIME_SAT = END_TIME_SAT
        self.START_TIME_SUN = START_TIME_SUN
        self.END_TIME_SUN = END_TIME_SUN