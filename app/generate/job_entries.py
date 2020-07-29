import pandas as pd
import numpy as np
from app.generate.models.job_entries import get_job_entries_all


def determinate_working_hours(df:object):
    daily_blocks = (df
                .apply(lambda row: round(row['daily_blocks'] / 2 * row['weekly_work_days']), axis=1)
            )
    return  daily_blocks

def convert_datetime_to_str(df:object):
    start = (df
                .apply(lambda row:row['entrada'], axis=1)
                .apply(lambda start: str(start))
            )
    return  start

def job_entries(workers: pd, store_week_demand: pd,id_location_code: str):
    res_job_entries = pd.DataFrame(get_job_entries_all())
    fill_job_entries = res_job_entries['location_id'] == id_location_code
    res_job_entries_location = res_job_entries[fill_job_entries]
    h = workers[['name_contracts','daily_blocks','weekly_work_days']]
    h['working_hours'] = determinate_working_hours(df=h)
    tem_job_entries = h.merge(res_job_entries_location, left_on = ['working_hours','weekly_work_days'], right_on = ['working_hours','work_days'], how = 'left')
    tem_job_entries = store_week_demand.merge(tem_job_entries, left_on = ['day_id'], right_on= ['weekday'], how = 'left').drop(['daily_blocks','weekly_work_days','working_hours','location_id','work_days','day_id','weekday'], axis=1)
    tem_job_entries['entrada'] = tem_job_entries['Fecha'].astype(str) + ' ' + tem_job_entries['hour'].astype(str)
    tem_job_entries = tem_job_entries[['name_contracts','entrada']]
    tem_job_entries = tem_job_entries.rename(columns={'name_contracts':'nombre'})
    tem_job_entries['entrada'] = convert_datetime_to_str(df=tem_job_entries)
    tem_job_entries= tem_job_entries.dropna()
    data = {
        "columns":  tem_job_entries.columns.values.tolist(),
        "data": tem_job_entries.values.tolist()
    }

    return data

