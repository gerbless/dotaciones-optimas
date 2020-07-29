import pandas as pd
from app.log.main import log
from app.generate.models.daily_constraints import get_daily_constraints_all

def convert_date_to_str(df:object):
    date = (df
                .apply(lambda row:row['fecha'], axis=1)
                .apply(lambda date: str(date))
            )
    return  date  

def daily_constraints(week_demand: pd, id_location_code= str):
    result_daily_constraints =  pd.DataFrame(get_daily_constraints_all())
    #week_demand['day_id']  = pd.to_datetime(week_demand.loc[:,('Fecha')], format="%Y-%m-%d").dt.weekday
    week_demand = pd.DataFrame(week_demand,columns=['Fecha','day_id'])
    week_demand['Tienda']= id_location_code

    result_daily_constraints = result_daily_constraints.merge(week_demand, left_on=['day_id'], right_on=['day_id'], how = 'left').drop(['day_id'], axis=1)
    result_daily_constraints = result_daily_constraints[['name_contracts','Fecha','type']]
    result_daily_constraints = result_daily_constraints.rename(columns={'name_contracts':'nombre','Fecha':'fecha','type':'tipo'})
    result_daily_constraints['fecha'] = convert_date_to_str(df=result_daily_constraints)
    data = {
        "columns": result_daily_constraints.columns.values.tolist(),
        "data": result_daily_constraints.values.tolist()
    }
    return data, week_demand