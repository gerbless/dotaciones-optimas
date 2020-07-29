from app.enviroment_config import EnvSisaPgConfig, EnvPq0Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData

mymetadata_generate_process = MetaData(schema='demand_process')
mymetadata_forecast = MetaData(schema='forecast')
mymetadata = MetaData()
Base = declarative_base(metadata=mymetadata)
engine = None
session = None


mymetadata_hana= MetaData(schema=EnvPq0Config.PQ0_USER)
mymetadata_hana = MetaData()
BaseHana = declarative_base(metadata=mymetadata_hana)
engineHana = None
sessionHana = None

class connection():
    engine = create_engine(EnvSisaPgConfig.SISA_PG_DATABASEURL)
    Session = sessionmaker(bind=engine)
    session = Session()

class connection_transactions():
    engine = create_engine(EnvSisaPgConfig.SISA_PG_DATABASEURL)
    SessionTransactions = sessionmaker(bind=engine, autocommit=True)
    session_transactions = SessionTransactions()

class connectionHana():
    engineHana = create_engine('hana://{}:{}@{}:{}'.format(EnvPq0Config.PQ0_USER,EnvPq0Config.PQ0_PASS,EnvPq0Config.PQ0_HOST,EnvPq0Config.PQ0_PORT))
    Session = sessionmaker(bind=engineHana)
    sessionHana = Session()