class Elogs:

    def __init__(self, id_control_of_process: int, level:str, message:str,  created: str):
        self.id_control_of_process = id_control_of_process
        self.level = level
        self.message = message
        self.created = created