import logging
from app.generate.demand import demand
from app.generate.endowments import endowments
from app.generate.workers import workers
from app.generate.daily_constraints import daily_constraints
from app.generate.job_entries import job_entries
from app.generate.launch_entries import launch_entries
from app.log.main import log
from app.helpers.util import correct_demand

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def generate(id_process: int, location_codes: object, dates_search: dict, id_location:int):
    logger.info('DEMAND')
    format_demand_json, blocks, switch_code_local, mirror = demand(id_process=id_process, location_codes=location_codes, dates_search=dates_search)
    print("ES LOCAL ESPEJO: {}".format(mirror))
    format_demand_json['data'], week_demand = correct_demand(data=format_demand_json['data'])
    logger.info('WORKERS')
    result_workers_json, result_workers = workers()
    logger.info('ENDOWMENTS')
    result_endowments_json = endowments(id_location=id_location, dates_search=dates_search)
    logger.info('DAILY CONSTRAINTS')
    result_daily_constraints, store_week_demand = daily_constraints(week_demand=week_demand,id_location_code=location_codes.code)
    logger.info('JOB ENTRIES')
    result_job_entries = job_entries(workers=result_workers, store_week_demand=store_week_demand,id_location_code=location_codes.code)
    logger.info('LAUNCH ENTRIES')
    result_launch_entries = launch_entries(blocks=blocks)
    print("1.result_endowments_json {} ----- {}".format(result_endowments_json['data'],len(result_endowments_json['data'])))
    print("2.format_demand_json {} ----- {}".format(format_demand_json['data'],len(format_demand_json['data'])))
    print("3.result_workers_json {} ----- {}".format(result_workers_json['data'],len(result_workers_json['data'])))
    print("4.result_launch_entries {} ----- {}".format(result_launch_entries['data'],len(result_launch_entries['data'])))
    print("5.result_daily_constraints {} ----- {}".format(result_daily_constraints['data'],len(result_daily_constraints['data'])))
    print("6.result_job_entries {} ----- {}".format(result_job_entries['data'],len(result_job_entries['data'])))

    #validaciones necesarias.
    if len(result_endowments_json['data']) == 0:
        raise ValueError ('Lock del input se encuentra sin datos.')
    elif len(format_demand_json['data']) == 0:
        raise ValueError ('Demanda se encuenta sin datos.')
    elif len(result_workers_json['data']) == 0:
        raise ValueError ('Trabajadores se encuenta sin datos.')
    elif len(result_launch_entries['data']) == 0:
        raise ValueError ('lunch entries se encuenta sin datos.')
    elif len(result_daily_constraints['data']) == 0:
        raise ValueError ('Dias Restringidos se encuenta sin datos.')
    elif len(result_job_entries['data']) == 0:
        raise ValueError ('Horarios de Entrada se encuenta sin datos.')

    #raise ValueError ('SE PARO ACÁ')

    data = {
        "search_problem_data": {
            "Demanda": format_demand_json,
            "Trabajadores": result_workers_json,
            "lunch entries":result_launch_entries,
            "Lock": result_endowments_json,
            "Dias Restringidos": result_daily_constraints,
            "Horarios de Entrada" : result_job_entries,
            "Horas Restringidas":{
                "columns": [
                    "nombre",
                    "inicio",
                    "fin"
                ],
                "data":[]
            },
            "lunch_count_as_work": False,
            "store": location_codes.code,
            "modelo_optimizacion": "continuous",
            "max_iterations": 2
        }
    }

    return data
