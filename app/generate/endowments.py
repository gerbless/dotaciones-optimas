import pandas as pd
from app.log.main import log
from app.generate.models.endowments import get_endowments


def determinate_months(dates_search: dict):
    if dates_search['months'] == 12:
        raw = [1,13]
    else:
        raw = [int(dates_search['start'].split('-')[1]) ,int(dates_search['end'].split('-')[1]) + 1]

    months = []
    for x in range(raw[0],raw[1]):
        months.append("_{}".format(x))

    return months

def format_json(dot_Finaly: pd):
    dot_Finaly = dot_Finaly.rename(columns= {
            'code':'Tienda',
            'name_register':'nombre',
            'quantity':'Cantidad'})

    data = {
        "columns": dot_Finaly.columns.values.tolist(),
        "data": dot_Finaly.values.tolist()
    }

    return data

def endowments(id_location:int, dates_search: dict):
    dot = pd.DataFrame(get_endowments(store=id_location).\
        fetchall(), columns = [
            'idx','store','code'
            ,'working_days_week_quantity',
            'working_hours_week_quantity',
            'contracts_types',
            'name_register',
            'hrs_sem',
            'quantity'])

    dot['0']=0
    months = determinate_months(dates_search=dates_search)
    meses_dot=pd.DataFrame({'mes':months}).astype(str)
    meses_dot['0']=0

    dot_Finaly=pd.merge(dot, meses_dot, on=['0'])
    dot_Finaly['code'] = dot_Finaly['code']
    dot_Finaly = dot_Finaly.drop(['mes','0','hrs_sem','contracts_types','working_hours_week_quantity','working_days_week_quantity','store','idx'],1)
    dot_Finaly = dot_Finaly.sort_values(by=['code'], ascending=True)
    dot_Finaly = dot_Finaly.reset_index(drop=True)
    data = format_json(dot_Finaly=dot_Finaly)
    return data

def i(a,name):
    a.to_csv(name)