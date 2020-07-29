class ElaunchEntries():

    def __init__(self, title:str, start:str, end:str, is_active:bool, created:str=None, updated:str=None):
        self.title = title
        self.start = start
        self.end = end
        self.is_active = is_active
        self.created = created
        self.updated = updated