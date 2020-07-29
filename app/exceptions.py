from app.enviroment_config import EnvironmentConfig


class InvalidControlOfProcessEndowmentsException(Exception):
    def __init__(self, message_user: str, err_debug: str):
        self.error = err_debug
        self.message = message_user
        if EnvironmentConfig.MODE_DEBBUGER:
            print(self.error)

    def __str__(self):
        return self.message