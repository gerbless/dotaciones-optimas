import os
from dotenv import load_dotenv, find_dotenv


class EnvSisaPgConfig():
    load_dotenv(find_dotenv())
    SISA_PG_DATABASEURL = os.environ.get('SISA_PG_DATABASEURL')

class EnvPq0Config():
    load_dotenv(find_dotenv())
    PQ0_HOST = os.environ.get('PQ0_HOST')
    PQ0_PORT = os.environ.get('PQ0_PORT')
    PQ0_USER = os.environ.get('PQ0_USER')
    PQ0_PASS = os.environ.get('PQ0_PASS')

class EnvironmentConfig():
    load_dotenv(find_dotenv())
    MODE_DEBBUGER = os.environ.get('MODE_DEBBUGER')
    COUNT_SCHEDULING = os.environ.get('COUNT_SCHEDULING')
    MAX_ATTEMPTS= os.environ.get('MAX_ATTEMPTS')
    URL_SEARCH_MODEL= os.environ.get('URL_SEARCH_MODEL')
    MAX_ATTEMPTS_REQUEST_INPUT= os.environ.get('MAX_ATTEMPTS_REQUEST_INPUT')