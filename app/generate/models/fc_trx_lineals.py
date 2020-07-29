
from app.connect import connectionHana, BaseHana, mymetadata_hana
from sqlalchemy import Table,Integer, Column, create_engine, Integer, String, DateTime, Boolean, func, Sequence, exists
from sqlalchemy.sql import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import mapper

def get_transactional_data(id_location: str,dates: tuple):
    sql = text("""SELECT LOCATION_ID, TRAN_START_DT, HOUR AS HORA, Q_TRX,
               CAST(CASE WHEN ((PROM_TIME + PROM_ITIME) * Q_TRX)/1800 <= 4 THEN
                 ((PROM_TIME + PROM_ITIME) * Q_TRX)/(1800*0.9) ELSE
                 ((PROM_TIME + PROM_ITIME) * Q_TRX)/(1800*0.8) END AS float) AS CAJERO_EQ
               FROM PQ0.CHI_SIS_FLEX.FC_TRX_LINEALS WHERE LOCATION_ID=:id_location
               AND TRAN_START_DT BETWEEN :date_start AND :date_end """)

    return connectionHana.sessionHana.execute(sql, {"id_location":id_location,
                                        "date_start":dates[0],
                                        "date_end":dates[1]})

