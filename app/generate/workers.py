import pandas as pd
from app.log.main import log
from app.generate.models.endowments_optimization_contracts import get_endowments_optimization_contracts_all

def format_json(result_workers: pd):
    coll_names = columns_name(result_workers=result_workers)
    data = {
        "columns": coll_names.columns.values.tolist(),
        "data": result_workers.values.tolist()
    }
    return data

def columns_name(result_workers: pd):
    result_workers = result_workers.rename(columns= {
            'name_contracts':'nombre',
            'daily_blocks':'bloques diarios',
            'weekly_work_days':'dias de trabajo semanal',
            'fixed_week':'semana fija',
            'cost_monday':'costo lunes',
            'cost_tuesday':'costo martes',
            'cost_wednesday':'costo miercoles',
            'cost_thursday':'costo jueves',
            'cost_friday':'costo viernes',
            'cost_saturday':'costo sabado',
            'cost_sunday':'costo domingo',
            'contract':'contratar',
            'permanent':'Fijo'})

    return result_workers

def resplaceBol(df:object):
    fixed_week = (df
                .apply(lambda row: row['fixed_week'], axis=1)
                .apply(lambda fixed_week: 1 if fixed_week is True else 0)
             )
    df['fixed_week'] = fixed_week
    return df

def workers():
    result_workers = pd.DataFrame(get_endowments_optimization_contracts_all())
    result_workers = resplaceBol(df=result_workers)
    result_workers= result_workers.drop(['id_optimization_contracts', 'created','updated'], axis=1)
    result_workers = result_workers[
        [
            'name_contracts',
            'daily_blocks',
            'weekly_work_days',
            'fixed_week',
            'cost_monday',
            'cost_tuesday',
            'cost_wednesday',
            'cost_thursday',
            'cost_friday',
            'cost_saturday',
            'cost_sunday',
            'contract',
            'permanent'
        ]
    ]
    result_workers_json = format_json(result_workers=result_workers)

    return result_workers_json, result_workers