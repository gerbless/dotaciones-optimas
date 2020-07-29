import pandas as pd
import numpy as np
from app.generate.models.launch_entries import get_launch_entries_all
from app.helpers.util import *

def format_json(df: object):
    valuesIndex = []
    format_launch_entries = []
    for ix in df.index:
        valuesHour = []
        valuesIndex.append([ix,df.loc[ix]])
        valuesHour.append(ix)
        for x in valuesIndex[0][1]:
            valuesHour.append(int(x))
        valuesIndex = []
        format_launch_entries.append(valuesHour)

    nameColums = []
    nameColums.append('max_break_start')
    for x in df.columns:
        nameColums.append('{:%H:%M}'.format(x))

    obj ={
        "columns": nameColums,
        "data": format_launch_entries
    }

    return obj

def launch_entries(blocks:pd):
    hours = pd.DataFrame()
    res_job_entries = pd.DataFrame(get_launch_entries_all())
    hours['hora'] = np.unique(blocks['hora'])
    hours['tmp'] = 1
    res_job_entries['tmp'] = 1
    res_job_entries = pd.merge(res_job_entries,hours, on=['tmp'])
    res_job_entries= validate_range(res_job_entries)
    res_job_entries['hora'] = pd.to_datetime(res_job_entries.loc[:,('hora')]).dt.time
    res = pd.pivot_table(res_job_entries, index = ['title'], columns='hora', values='existe').fillna(0)
    data = format_json(df=res)

    return data

def i(a,name):
    a.to_csv(name)
