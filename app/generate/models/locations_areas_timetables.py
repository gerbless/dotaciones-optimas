from app.connect import connection, mymetadata_forecast
from sqlalchemy import Table,Integer, Column, Integer, String, Sequence
from sqlalchemy.sql import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import mapper
from app.generate.entities.locations_area_timetable import ElocationsAreaTimetable

locationsAreaTimetable = Table('LOCATIONS_AREAS_TIMETABLES', mymetadata_forecast,
            Column('ID_LOCATION_AREA_TIMETABLE', Integer, Sequence('forecast.LOCATIONS_AREAS_TIMETABLES_ID_LOCATION_AREA_TIMETABLE_seq'), primary_key=True, nullable=False),
            Column('LOCATION_ID',Integer, nullable=False),
            Column('PRE_OPEN_TIME',Integer),
            Column('POST_CLOSE_TIME',Integer),
            Column('START_TIME_MON',String, nullable=False),
            Column('END_TIME_MON',String, nullable=False),
            Column('START_TIME_TUE',String, nullable=False),
            Column('END_TIME_TUE',String, nullable=False),
            Column('START_TIME_WED',String, nullable=False),
            Column('END_TIME_WED',String, nullable=False),
            Column('START_TIME_THU',String, nullable=False),
            Column('END_TIME_THU',String, nullable=False),
            Column('START_TIME_FRI',String, nullable=False),
            Column('END_TIME_FRI',String, nullable=False),
            Column('START_TIME_SAT',String, nullable=False),
            Column('END_TIME_SAT',String, nullable=False),
            Column('START_TIME_SUN',String, nullable=False),
            Column('END_TIME_SUN',String, nullable=False)
        )

mapper(ElocationsAreaTimetable, locationsAreaTimetable)

def get_locations_area_timetable_all():
    return connection.session.query(locationsAreaTimetable).all()

def get_get_locations_area_timetable_by_location(id_location: str):
    sql = connection.session.query(ElocationsAreaTimetable).\
       filter(ElocationsAreaTimetable.LOCATION_ID == id_location)

    return connection.session.execute(sql)