class Einput:
    def __init__(self, taks_id:str ,input_json: object,is_active: bool,last_month_id:int, attempts:int, created: str,updated: str = None):

      self.taks_id = taks_id
      self.input_json = input_json
      self.is_active = is_active
      self.last_month_id = last_month_id
      self.attempts = attempts
      self.created = created
      self.updated = updated