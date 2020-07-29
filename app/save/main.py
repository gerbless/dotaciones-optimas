from app.save.entities.endowments_optimizer import EendowmentsOptimizer
from app.save.models.endowments_optimizer import add_endowments_optimizer
from app.generate.models.endowments_optimization_contracts import get_endowments_optimization_contracts_all
from app.helpers.util import *

def save_endowments_optimizer(data: object, info: object):
    year = int(moment.date(info.last_month.date_month_start).add(years=1).format(fy))
    month = int(moment.date(info.last_month.date_month_start).format(fm))
    endowmentsOptimizer =EendowmentsOptimizer(info.taks_id, year, month, data['best_parameters']['Contracts'], data['best_parameters']["Cost"], data['best_parameters']["TNC"], data['best_parameters']["Store"], data['best_parameters']["Process_time"], fn_now_ff_hh())
    endowments_optimization_contracts = get_endowments_optimization_contracts_all()
    add_endowments_optimizer(endowments_optimizer=endowmentsOptimizer, endowments_optimization_contracts=endowments_optimization_contracts, contracts=data['best_parameters']['Contracts'])
    print('GENERADO PROCESO CON EXITO')
    #raise ValueError ('paro al final')