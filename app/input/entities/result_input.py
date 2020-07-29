class Eresult_input:
    def __init__(self, id_taks: str, input_id: int, state: str, types: str, message: str, traceback: str, result: object, created: str):
      self.id_taks = id_taks
      self.input_id = input_id
      self.state = state
      self.types = types
      self.message = message
      self.traceback = traceback
      self.result = result
      self.created = created