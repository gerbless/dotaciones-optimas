import logging
import math
from app.enviroment_config import EnvironmentConfig
from app.scheduling.models.locations import get_locations, get_num_locations, get_location_by_id
from app.scheduling.entities.control_of_process_endowments import EcontrolOfProcessEndowments
from app.generate.entities.last_month import ElastMonth
from  app.scheduling.models.control_of_process_endowments import  get_num_control_of_process_endowments_for_month, add_control_of_process_endowments_for_month, get_exists_filter, get_select_schedules, update_activity_pross, get_activity_schedules
from app.generate.models.last_month import get_last_month_by_code, add_last_month, delete_last_month_by_date
from app.generate.main import generate
from app.input.main import search_model
from app.helpers.util import *
from app.log.main import log

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ask_if_you_should_schedule(monthyear:int):
    return get_num_control_of_process_endowments_for_month(monthyear=monthyear)

def create_scheduling_by_location(monthyear:int, num_cases: int):
    count = 0
    day_week = 0
    count_scheduling = int(EnvironmentConfig.COUNT_SCHEDULING)

    if num_cases > count_scheduling:
        count_scheduling = num_cases
        logger.info('Número de agendamientos por día será cercano a  {}'.format(count_scheduling))
    for row in get_locations():
        if count >= count_scheduling:
            count = 0
            day_week+=1

        if get_exists_filter(monthyear=monthyear, id_location=row['id_location']) is 0:

            scheduling = today_ff_add_days(day=day_week)
            data = EcontrolOfProcessEndowments(row['id_location'],
                                            scheduling,
                                            0,
                                            False,
                                            monthyear,
                                            1,
                                            fn_now_ff_hh(),
                                            fn_now_ff_hh())

            add_control_of_process_endowments_for_month(data=data)
            count+=1

def scheduling(monthyear: int):
    logger.info('Inicio consulta proceso agendamiento {}'.format(now_ff))
    num_control_process = ask_if_you_should_schedule(monthyear=monthyear)
    num_locations = get_num_locations()

    print(last_month_day)
    print(today_day)
    print(num_control_process)
    print(num_locations)
    if num_control_process < num_locations:
        remaining_days = last_month_day - today_day

        num_cases = (num_locations - num_control_process) / remaining_days
        logger.info('Iniciar procesos de agendamiento para locales. [Agendados:{} - Locales:{}]'.format(num_control_process,num_locations))
        create_scheduling_by_location(monthyear=monthyear, num_cases= math.ceil(num_cases))
        logger.info('Se encontraron loscales y se realizó agendamientos')
    logger.info('::: FIN DE AGENDAMIENTOS :::')

def delete_last(dates_search: dict, id_location_code= str):
    delete_last_month_by_date(start=dates_search['start'], end=dates_search['end'], code=id_location_code)

def roll_back_pross(idx: int):
    update_activity_pross(idx,{EcontrolOfProcessEndowments.execution_process: False, EcontrolOfProcessEndowments.activity: 1, EcontrolOfProcessEndowments.updated:fn_now_ff_hh()})

def create_last_month(id_control_of_process: int, dates_search: dict,id_location_code: str):
    data = ElastMonth(id_control_of_process, dates_search['start'], dates_search['end'], dates_search['months'], id_location_code, fn_now_ff_hh(), False)
    add_last_month(data=data)

def activity_close(idx= int):
    update_activity_pross(idx,{EcontrolOfProcessEndowments.activity: 3, EcontrolOfProcessEndowments.updated:fn_now_ff_hh()})

def determine_month_to_search(id_location_code:str):
    lastMonth = get_last_month_by_code(code=id_location_code)
    annual =  True if lastMonth is None else False
    return determinate_previous_start_month_ff(annual=annual, lastMonth=lastMonth)

def diary_init(id_process:int, attempts: int, id_location:str):
    logger.info('Procesando agenda con ID:[{}]'.format(id_process))
    log((id_process,INFO, mesagges['pross_scheduling']))

    update_activity_pross(idx=id_process,data={EcontrolOfProcessEndowments.execution_process: True,
        EcontrolOfProcessEndowments.attempts:(attempts + 1),
        EcontrolOfProcessEndowments.activity: 2,
        EcontrolOfProcessEndowments.updated:fn_now_ff_hh()})

    logger.info('Buscando datos transaccionales ID:[{}]'.format(id_process))
    log((id_process,INFO, mesagges['pross_trass']))
    location_codes = get_location_by_id(idx=id_location)
    dates_search = determine_month_to_search(id_location_code=location_codes.code)
    log((id_process,INFO, mesagges['df_transaccionales']))

    return location_codes, dates_search

def check_activity(monthyear: int, scheduling:str):
    activity = get_activity_schedules(monthyear=monthyear)
    if scheduling != now_ff and activity > 0:
        exit()

def closet_diary(id_control_of_process:int,dates_search: dict, id_location_code:str):
    create_last_month(id_control_of_process=id_control_of_process, dates_search=dates_search, id_location_code=id_location_code)

def search_diary(monthyear: int, day: int = 0, attemps: int = 0):
    if day <= 60:
        if day <= 30:
            scheduling = today_ff_add_days(day=day)
            check_activity(monthyear=monthyear, scheduling=scheduling)
        else:
            attemps+=1
            monthyear = previous_monthyear
            scheduling = determinate_previous_scheduling(attemps=attemps)

        logger.info('Consultando agendamiento con date:[{}] y monthyear:[{}]'.format(scheduling,monthyear))
        schedules = get_select_schedules(monthyear=monthyear, scheduling=scheduling,config_attempts=EnvironmentConfig.MAX_ATTEMPTS).fetchone()

        if schedules is not None:
            closet = False # determina si el input fue creado y respaldado en la tabla last_month
            try:
                location_codes, dates_search = diary_init(id_process=schedules[0], attempts=schedules[3], id_location=schedules[1])
                for numMonths in range(0, int(dates_search['months'])):
                    closet = False
                    month_to_month = incremet_month(date=dates_search['start'], num_month=numMonths)
                    logger.info('GENERANDO CON FECHA DESDE {} HASTA {}'.format(month_to_month['start'],month_to_month['end']))
                    log((schedules[0],INFO, mesagges['month_to_month'].format(month_to_month['start'],month_to_month['end'])))

                    input_data= generate(id_process=schedules[0], location_codes=location_codes, dates_search=month_to_month, id_location=schedules[1])
                    closet_diary(id_control_of_process=schedules[0],dates_search=month_to_month, id_location_code=location_codes.code)
                    closet = True
                    search_model(input=input_data, control_of_process_id=schedules[0], dates_search=month_to_month,id_location_code=location_codes.code)

                activity_close(idx=schedules[0])

            except Exception as e:
                roll_back_pross(idx=schedules[0])
                if closet is True:
                    delete_last(dates_search=month_to_month, id_location_code=location_codes.code)

                log((schedules[0],ERR,str(e)))
                logger.error(' En el proceso ID {} intento Nro {}. TIPO: {}'.format(schedules[0],schedules[3] + 1,e))
        else:
            day+=1
            search_diary(monthyear,day, attemps)