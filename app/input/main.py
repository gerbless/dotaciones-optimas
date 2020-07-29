import os
import json
import requests
import logging
from app.helpers.util import *
from app.enviroment_config import EnvironmentConfig
from app.input.models.input import add_input, get_endowments_result, update_input, delete_input
from app.generate.models.last_month import get_last_month_by_date, get_recover, update_last_month
from app.generate.main import generate
from app.input.models.result_input import add_result_input, delete_result_input
from app.input.entities.input import Einput
from app.input.entities.result_input import Eresult_input
from app.save.main import save_endowments_optimizer
from app.log.main import log

url = EnvironmentConfig.URL_SEARCH_MODEL
max_request = int(EnvironmentConfig.MAX_ATTEMPTS_REQUEST_INPUT)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_input(data: object, task_id: str, dates_search: dict, id_location_code: str):
    last_month = get_last_month_by_date(start=dates_search['start'], end=dates_search['end'], code=id_location_code)
    add_input(data=Einput(task_id,data,True,last_month.id_last_month,0,fn_now_ff_hh(),fn_now_ff_hh()))

def update_state(id_input: int, data:dict):
    update_input(idx=id_input,data=data)

def search_model(input: object, control_of_process_id:int, dates_search: dict, id_location_code:str):
    headers = {'content-type': 'application/json'}
    r = requests.post("{}search_model".format(url), data=json.dumps(input), headers=headers)
    if r.status_code == 201:
        res = r.json()
        create_input(data=input, task_id=res['task_id'], dates_search=dates_search, id_location_code=id_location_code)
    else:
        r.raise_for_status()

def finished_work(id_input:int, task_id:str, result:object):
    add_result_input(data=Eresult_input(task_id, id_input,'SUCCESS', '', '', '', result, fn_now_ff_hh()))

def pross_error(id_input:int, task_id:str, types:str, message: str, traceback: str, result:object):
    add_result_input(data=Eresult_input(task_id, id_input,'ERROR-INPUT', types, message, traceback, result, fn_now_ff_hh()))

def state_management(data: object,id_input:int, attempts: int):
    stated = data['status']
    attempts+=1
    result = None
    print("{} -> {}".format(data['task_id'],stated))
    # El estado de la tarea es desconocido (se supone pendiente desde que conoce la identificación).
    if stated == 'PENDING':
        update_state(id_input=pross_task_id.id_input, data= {Einput.is_active: True, Einput.updated:fn_now_ff_hh()})
    # La tarea fue iniciada por un trabajador ( task_track_started).
    elif stated == 'STARTED':
        if max_request >= attempts:
            update_state(id_input=id_input, data= {Einput.is_active: True, Einput.created:fn_now_ff_hh(),Einput.updated:fn_now_ff_hh(), Einput.attempts: attempts})
            get_result_task_id()
        else:
            add_result_input(data=Eresult_input(data['task_id'], id_input,'TIMEOUT', 'Tiempo agotado','Número maximo de intentos [{}]'.format(max_request), '', data, fn_now_ff_hh()))

    #Tarea realizada
    elif stated == 'SUCCESS':
        if 'type' in data['result']:
            pross_error(id_input=id_input,task_id=data['task_id'],types=data['result']['type'],message=data['result']['message'],traceback=data['result']['traceback'],result=data['result'])
        elif 'best_parameters' in data['result']:
            finished_work(id_input=id_input,task_id=data['task_id'], result=data['result'])
            result = result=data['result']
        else:
            print(data)

    # Tarea fallida
    elif stated == 'FAILURE':
        add_result_input(data=Eresult_input(data['task_id'], id_input,'FAILURE', 'Tarea fallida', '', data, fn_now_ff_hh()))

    # La tarea fue revocada.
    elif stated == 'REVOKED':
        add_result_input(data=Eresult_input(data['task_id'], id_input,'REVOKED', 'La tarea fue revocada', '', data, fn_now_ff_hh()))

    return result

def get_result_task_id():
    pross_task_id = get_endowments_result()
    if pross_task_id is not None:
        delete_result_input(id_input=pross_task_id.id_input)
        update_state(id_input=pross_task_id.id_input,data= {Einput.is_active: False, Einput.updated:fn_now_ff_hh()})
        try:
            r = requests.get("{}{}".format(url,pross_task_id.taks_id))
            if r.status_code == requests.codes.ok:
                res =  state_management(data=r.json(),id_input=pross_task_id.id_input, attempts=pross_task_id.attempts)
                if res is not None:
                    save_endowments_optimizer(data=res,info=pross_task_id)
            else:
                update_state(id_input=pross_task_id.id_input, data= {Einput.is_active: True, Einput.updated:fn_now_ff_hh()})
                r.raise_for_status()
        except Exception as e:
            print(e)
            update_state(id_input=pross_task_id.id_input, data= {Einput.is_active: True, Einput.updated:fn_now_ff_hh()})

def processing_errors():
    try:
        data = get_recover()
        if data is not None:
            update_last_month(idx=data.id_last_month, data={'recover':False})
            dates_search = {'start':data.date_month_start.strftime("%Y-%m-%d"),'end':data.date_month_end.strftime("%Y-%m-%d"),'months':1}
            input_data = generate(id_process=data.id_control_of_process_endowments, id_location_code=data.code, dates_search=dates_search, id_location=data.control_process.id_location)
            delete_result_input(id_input=data.input.id_input)
            delete_input(idx=data.input.id_input)
            search_model(input=input_data, control_of_process_id=data.id_control_of_process_endowments, dates_search=dates_search,id_location_code=data.code)
    except Exception as e:
        if data is not None:
            update_last_month(idx=data.id_last_month, data={'recover':True})
        print(e)