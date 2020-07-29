import numpy as np
import pandas as pd
from pandasql import sqldf
import moment
from app.helpers.util import *
from app.generate.models.fc_trx_lineals import get_transactional_data
from app.log.main import log
from datetime import datetime, timedelta
from app.generate.models.locations_areas_timetables import get_locations_area_timetable_all
from app.generate.models.post import get_posts

#DESDE LA FECHA ACTUAL VA 15 MESES PARA ATRAS
def dates_filter_growth_factor(id_process:int):
    start = moment.now().subtract(years=2,months=3).replace(day=1).format(ff)
    end = moment.now().format(ff)
    log((id_process,INFO, mesagges['ff_cal_fc'].format(start,end)))

    return start, end

#para tomar los meses a filtrar:
def dates_filter_months(id_process:int, dates_search: dict):
    #start = moment.now().subtract(years=2).replace(day=1).format(ff)
    #end = moment.now().format(ff)
    data = pd.DataFrame({'day': [dates_search['start']]})
    data['day'] = pd.to_datetime(data['day'], format="%Y-%m-%d")
    data['day'] = data.\
        day.dt.to_period("W-SUN").apply(lambda x: x.start_time)
    start_week = str(data.loc[0,'day'])
    log((id_process,INFO, mesagges['ff_filter_months'].format(start_week[:10],dates_search['end'])))
    return datetime.strptime(start_week[:10], '%Y-%m-%d'), datetime.strptime(dates_search['end'], '%Y-%m-%d'), int(dates_search['start'][5:7])

def transactional(id_location: str, id_process:int):
    dates = dates_filter_growth_factor(id_process=id_process)
    transactional = get_transactional_data(id_location=id_location, dates=dates)
    pd_transactional = pd.DataFrame(transactional.fetchall())
    pd_transactional.rename(columns={0: 'LOCATION_ID', 1:
                        'TRAN_START_DT',
                        2: 'HORA',
                        3: 'Q_TRX',
                        4: 'CAJERO_EQ'}, inplace=True)
    return pd_transactional, dates

#calcula factor de crecimiento
def calculate_growth_factor(factor):
    factor["factor_crec"] = factor["CAJERO_EQ_x"]/factor["CAJERO_EQ_y"]-1
    factor = factor.replace(np.inf, 0)
    factor["factor_0"] = 0
    factor["factor_crec"] = factor[["factor_crec","factor_0"]].max(axis=1)
    factor = factor.groupby(['LOCATION_ID']).mean().reset_index().drop(["dia_y","dia_x","anio_y","anio_x",'Q_TRX_x','Q_TRX_y','factor_0','mes'], axis=1)
    return factor

#aplica factor de crecimiento
def apply_growth(df, factor, id_process:int, dates_search: dict):
    dates = dates_filter_months(id_process=id_process, dates_search=dates_search)
    trx_1year = df[(df['ds'] >= dates[0].date()) & (df['ds'] <= dates[1].date())]
    trx_1year = pd.merge(trx_1year, factor, left_on = 'LOCATION_ID', right_on = 'LOCATION_ID').drop(['CAJERO_EQ_x','CAJERO_EQ_y'], axis=1)
    trx_1year['ce_var'] = trx_1year['CAJERO_EQ'] * (1 + trx_1year['factor_crec'])
    trx_1year['ds'] = pd.to_datetime(trx_1year['ds'])
    return trx_1year.sort_values(by=['ds']), dates[2]

#generar bloques
def generate_blocks():
    blocks = (pd.DataFrame(columns=['hour'],
                  index=pd.date_range(moment.now().\
                      replace(hours=0, minutes=0, seconds=0).\
                          format(ff_hh), moment.now().\
                      replace(hours=23, minutes=30, seconds=0).\
                          format(ff_hh),freq='30T'))
       .between_time('00:00','23:30').reset_index())

    blocks[['fecha','hora']]=blocks.loc[:,('index')].\
        astype(str).str.split(" ", expand=True)

    blocks[['h','m','s']]=blocks.loc[:,("hora")].\
        astype(str).str.split(":", expand=True).astype(int)

    blocks = sqldf('''select case when m > 0 then h || ":"|| m || ":0"|| s else
                    h || ":0"|| m || ":0"|| s  end as hora
                    from blocks''')
    return blocks

#generar fechas de bloques
def generate_blocks_dates(apply_factor, blocks):
    stores = pd.DataFrame()
    stores['LOCATION_ID'] = np.unique(apply_factor['LOCATION_ID'])
    stores['tmp'] = 1

    dates = pd.DataFrame()
    dates['TRAN_START_DT'] = np.unique(apply_factor['TRAN_START_DT'])
    dates['tmp'] = 1

    hours = pd.DataFrame()
    hours['HORA'] = np.unique(blocks['hora'])
    hours['tmp'] = 1

    blocks_dates = pd.merge(stores,dates, on=['tmp'])
    blocks_dates = pd.merge(blocks_dates,hours, on=['tmp'])

    blocks_dates['HORA'] = pd.to_datetime(blocks_dates['HORA'],format= '%H:%M:%S' ).dt.time
    apply_factor['HORA'] = pd.to_datetime(apply_factor['HORA'],format= '%H:%M' ).dt.time
    apply_factor = blocks_dates.merge(apply_factor, left_on=['LOCATION_ID','TRAN_START_DT','HORA'], right_on=['LOCATION_ID','TRAN_START_DT','HORA'], how = 'left').drop(['tmp'], axis=1)
    return apply_factor, blocks_dates

#definición rangos horarios con demanda
def definition_hourly_ranges_with_demand(apply_factor):
    blocks = generate_blocks()
    apply_factor, blocks_dates  = generate_blocks_dates(apply_factor=apply_factor, blocks=blocks)
    return apply_factor, blocks_dates, blocks

# selecciona semana de alta demanda de cada mes
def select_high_demand_week_of_each_month(ranges_with_demand_and_factor:pd , month:int):
    ranges_with_demand_and_factor['ds'] = pd.to_datetime(ranges_with_demand_and_factor['ds'], errors='coerce')
    ranges_with_demand_and_factor["week_start"] = ranges_with_demand_and_factor.\
        ds.dt.to_period("W-SUN").apply(lambda x: x.start_time)

    # enumerar demanda de canda semana
    weeks_high_demand=ranges_with_demand_and_factor.groupby(["week_start","LOCATION_ID"]).\
        agg({'ce_var': sum }).reset_index()

    # creacion de columnas de año, mes, dia
    weeks_high_demand[["anio","mes","dia"]]=weeks_high_demand.loc[:,("week_start")].\
        astype(str).str.split("-", expand=True).astype(int)
    weeks_high_demand['mes'] = month

    # se elige la semana de mayores transacciones con agrupacion por local, mes
    weeks_higher_transactions = pd.pivot_table(weeks_high_demand, values=['ce_var'], index=['LOCATION_ID','mes'],aggfunc= max).\
        reset_index()

    # en caso de agrupar dos semanas con transacciones maximas para un mes.
    # elimina la semana mas antigua
    weeks_higher_transactions = weeks_higher_transactions.drop_duplicates(["mes","ce_var"], keep="last")

    #USAR JOIN PARA TRAER LA COLUMNA DE  FECHA WEEK START Y DIA
    trx_weeks_higher_transactions = weeks_higher_transactions.merge(weeks_high_demand[["ce_var",'mes','week_start']], on=["ce_var",'mes'], how = 'left').\
        drop_duplicates(["mes","ce_var"], keep="last")

    trx_high_demand_weeks = sqldf('''select b.location_id, a.tran_start_dt, a.ds, a.hora, a.week_start, a.q_trx, a.cajero_eq, a.factor_crec, a.ce_var
        from ranges_with_demand_and_factor a
        left join trx_weeks_higher_transactions b
        on a.location_id = b.location_id
        and a.week_start = b.week_start
        where a.week_start in (select distinct week_start from trx_weeks_higher_transactions)
        and b.location_id in (select distinct location_id from trx_weeks_higher_transactions)
        ''')

    trx_high_demand_weeks['ds'] = pd.to_datetime(trx_high_demand_weeks['ds'])
    trx_high_demand_weeks['diasem'] = trx_high_demand_weeks.loc[:,('ds')].dt.weekday
    trx_high_demand_weeks = trx_high_demand_weeks.drop(['TRAN_START_DT','Q_TRX','CAJERO_EQ','factor_crec'], axis =1)

    return trx_high_demand_weeks

#filtra según funcionamiento de las tiendas,
# considerando tiempos de pre-apertura y post-cierre
def filter_according_to_preopening_and_postclosing(id_location: str):
    locations_area_timetable = pd.DataFrame(get_locations_area_timetable_all())
    locations_area_timetable = locations_area_timetable[locations_area_timetable['LOCATION_ID'] == id_location]

    locations_area_timetable['POST_CLOSE_TIME'] = locations_area_timetable.apply(corrige_post,axis=1)
    #apertura_cierre2=apertura_cierre
    locations_area_timetable.columns = locations_area_timetable.columns.str.replace("START_TIME_", "i_") #inicio jornada
    locations_area_timetable.columns = locations_area_timetable.columns.str.replace("END_TIME_", "f_") # fin jornada
    locations_area_timetable = locations_area_timetable[locations_area_timetable['PRE_OPEN_TIME'] >= 0]

    ### lun 
    locations_area_timetable['i_lun_d1']= locations_area_timetable.apply(inicio_lun_dia1,axis=1)
    locations_area_timetable['f_lun_d1']= locations_area_timetable.apply(fin_lun_dia1,axis=1)
    locations_area_timetable['i_mar_d2']= locations_area_timetable.apply(inicio_lun_dia2,axis=1)
    locations_area_timetable['f_mar_d2']= locations_area_timetable.apply(fin_lun_dia2,axis=1)

    ### mar
    locations_area_timetable['i_mar_d1']= locations_area_timetable.apply(inicio_mar_dia1,axis=1)
    locations_area_timetable['f_mar_d1']= locations_area_timetable.apply(fin_mar_dia1,axis=1)
    locations_area_timetable['i_mie_d2']= locations_area_timetable.apply(inicio_mar_dia2,axis=1)
    locations_area_timetable['f_mie_d2']= locations_area_timetable.apply(fin_mar_dia2,axis=1)

    ### mie
    locations_area_timetable['i_mie_d1']= locations_area_timetable.apply(inicio_mie_dia1,axis=1)
    locations_area_timetable['f_mie_d1']= locations_area_timetable.apply(fin_mie_dia1,axis=1)
    locations_area_timetable['i_jue_d2']= locations_area_timetable.apply(inicio_mie_dia2,axis=1)
    locations_area_timetable['f_jue_d2']= locations_area_timetable.apply(fin_mie_dia2,axis=1)

    ### jue
    locations_area_timetable['i_jue_d1']= locations_area_timetable.apply(inicio_jue_dia1,axis=1)
    locations_area_timetable['f_jue_d1']= locations_area_timetable.apply(fin_jue_dia1,axis=1)
    locations_area_timetable['i_vie_d2']= locations_area_timetable.apply(inicio_jue_dia2,axis=1)
    locations_area_timetable['f_vie_d2']= locations_area_timetable.apply(fin_jue_dia2,axis=1)

    ### vie
    locations_area_timetable['i_vie_d1']= locations_area_timetable.apply(inicio_vie_dia1,axis=1)
    locations_area_timetable['f_vie_d1']= locations_area_timetable.apply(fin_vie_dia1,axis=1)
    locations_area_timetable['i_sab_d2']= locations_area_timetable.apply(inicio_vie_dia2,axis=1)
    locations_area_timetable['f_sab_d2']= locations_area_timetable.apply(fin_vie_dia2,axis=1)

    ### sab
    locations_area_timetable['i_sab_d1']= locations_area_timetable.apply(inicio_sab_dia1,axis=1)
    locations_area_timetable['f_sab_d1']= locations_area_timetable.apply(fin_sab_dia1,axis=1)
    locations_area_timetable['i_dom_d2']= locations_area_timetable.apply(inicio_sab_dia2,axis=1)
    locations_area_timetable['f_dom_d2']= locations_area_timetable.apply(fin_sab_dia2,axis=1)

    ### dom
    locations_area_timetable['i_dom_d1']= locations_area_timetable.apply(inicio_dom_dia1,axis=1)
    locations_area_timetable['f_dom_d1']= locations_area_timetable.apply(fin_dom_dia1,axis=1)
    locations_area_timetable['i_lun_d2']= locations_area_timetable.apply(inicio_dom_dia2,axis=1)
    locations_area_timetable['f_lun_d2']= locations_area_timetable.apply(fin_dom_dia2,axis=1)
    return locations_area_timetable

#MARCA BLOQUES HABILES
def brand_skillable_bloks(blocks_dates, hours_preopening_and_postclosing):
    blocks_dates['ds'] = pd.to_datetime(blocks_dates['TRAN_START_DT'])
    week_24_7 = blocks_dates
    week_24_7['diasem'] = week_24_7.loc[:,('ds')].dt.weekday   # 0:lunes - 6:domingo
    week_24_7['HORA_fmto'] = pd.to_datetime(week_24_7['HORA'], format="%H:%M:%S")
    brand_skillable_blok = pd.merge(week_24_7, hours_preopening_and_postclosing, on='LOCATION_ID')
    #.drop(['PRE_OPEN_TIME','ID_LOCATION_AREA_TIMETABLE','POST_CLOSE_TIME','i_MON','f_MON','i_TUE','f_TUE','i_WED','f_WED','i_THU','f_THU','i_FRI','f_FRI','i_SAT','f_SAT','i_SUN','f_SUN'], axis=1)
    brand_skillable_blok['test_3']= brand_skillable_blok.apply(corrige_d,axis=1)
    return brand_skillable_blok

#REDEFINE DEMANDA EN BLOQUES HABILES
def redefines_demand_in_skillful_blocks(brand_skillable_bloks, trx_high_demand_weeks):
    filter_blocks = sqldf('''select location_id, ds, Hora, Hora_fmto
      , case when test_3 = 1 then 1 else 0 end bloque_habil
      from brand_skillable_bloks''')
    filter_blocks['ds_fmto'] = pd.to_datetime(filter_blocks.loc[:,('ds')], format="%Y-%m-%d")
    trx_high_demand_weeks['ds_fmto'] = pd.to_datetime(trx_high_demand_weeks.loc[:,('ds')], format="%Y-%m-%d")
    redefines_demand = trx_high_demand_weeks.merge(filter_blocks, left_on=['LOCATION_ID','ds_fmto','HORA'], right_on=['LOCATION_ID','ds_fmto','HORA'], how = 'left').drop([], axis=1)
    return redefines_demand

#setea min y max. min = 2. max = npos
def set_min_and_max_igual_two(redefines_demand, id_location: str):
    query_pos = get_posts(id_location=id_location).fetchone()
    if query_pos is None:
        npos = sqldf(''' select '{}' as local, 0 as tipo_caja '''.format(id_location))
    else:
        obj = {'local':[query_pos[0]],'tipo_caja':[query_pos[1]]}
        npos = pd.DataFrame(obj, columns =['local','tipo_caja'])


    redefines_demand_two = sqldf('''select location_id, ds, hora, week_start
              , case when dda > n_pos then n_pos else dda end dda
              from(
                      select location_id, ds_x as ds, hora, week_start
                      , case when bloque_habil = 1 and ce_var >= 2 then ce_var else 
                          case when bloque_habil = 1 and ce_var < 2 then 2 else  0 end end as dda
                      , tipo_caja n_pos
                      ,ce_var
                      from redefines_demand a
                      left join npos b
                      on a.location_id = b.local
                      where a.location_id in (select local from npos)
                ) t''')
    return redefines_demand_two

# agregar holgura y ausentismo - redondea hacia arriba
def absenteeism_and_slack(redefines_demand_two):
    redefines_demand_two['dda'] = (redefines_demand_two.loc[:,'dda']*1.15).apply(np.ceil)
    return redefines_demand_two

#dar formato requerido por el input
def format_demand(redefines_demand_two):
    redefines_demand_two["mes"]=pd.to_datetime(redefines_demand_two.loc[:,('week_start')]).dt.month
    #redefines_demand_two["Tienda"]=redefines_demand_two["location_id"]+"_"+redefines_demand_two["mes"].astype(str)
    redefines_demand_two["Tienda"]=redefines_demand_two["location_id"]
    redefines_demand_two['Fecha'] = pd.to_datetime(redefines_demand_two.loc[:,('ds')]).dt.date
    redefines_demand_two['hora'] = pd.to_datetime(redefines_demand_two.loc[:,('hora')]).dt.time
    result_demand = pd.pivot_table(redefines_demand_two,index = ["Tienda", "Fecha"], columns = "hora", values = "dda").fillna(0)
    demand_workers = redefines_demand_two[['Tienda','Fecha']]
    return result_demand, demand_workers

def preparad_json(result_demand:pd):
    valuesIndex = []
    formatDemand = []
    for ix in result_demand.index:
        valuesHour = []
        valuesIndex.append([ix[1],result_demand.loc[ix]])
        valuesHour.append('{:%Y-%m-%d}'.format(ix[1]))
        for x in valuesIndex[0][1]:
            valuesHour.append(int(x))
        valuesIndex = []
        formatDemand.append(valuesHour)

    nameColums = []
    horas = []
    nameColums.append('fecha')
    for x in result_demand.columns:
        horas.append('{:%H:%M}'.format(x))
        nameColums.append('{:%H:%M}'.format(x))

    blocks = pd.DataFrame({'hora': horas})
  

    obj ={
        "columns": nameColums,
        "data": formatDemand
    }

    return obj, blocks

#deferminar si el local cuenta con las transacciones pertinentes, encaso contrario de trabaja con local espejo
def determine_what_to_work_with_local(location_codes: object, id_process:int):
    pd_transactional, dates = transactional(id_location=location_codes.code, id_process=id_process)
    mirror = False
    if pd_transactional.size == 0:
        log((id_process,WAR, mesagges['df_null']))
        log((id_process,INFO, mesagges['location_mirror'].format(location_codes.location_mirror_code)))
        pd_transactional, dates = transactional(id_location=location_codes.location_mirror_code, id_process=id_process)
        mirror = True
    else:
        for x in range(0,16):
            start = moment.date(dates[0]).\
                add(months=x).\
                    format(ff)
            end = moment.date(dates[0]).add(months=x).\
                replace(day=calendar.monthrange(int(moment.date(dates[0]).\
                    add(months=x).format(fy)),int(moment.date(dates[0]).\
                        add(months=x).format(fm)))[1]).\
                            format(ff)
            pd_transactional['date'] = pd.to_datetime(pd_transactional['TRAN_START_DT'], format="%Y-%m-%d")
            num_register = pd_transactional[(pd_transactional['date'] >= start) & (pd_transactional['date'] <= end)].size
            print("{}  -  {}  -  {}".format(start,end,num_register))
            if num_register == 0:
                log((id_process,WAR, mesagges['df_null']))
                log((id_process,INFO, mesagges['location_mirror'].format(location_codes.location_mirror_code)))
                pd_transactional, dates = transactional(id_location=location_codes.location_mirror_code, id_process=id_process)
                mirror = True
                break

    return pd_transactional, mirror

# prepara datos factor de crecimiento
#crea tabla para calculo de factor de crecimiento: data_fc
def demand(id_process:int, location_codes: object, dates_search: dict):

    pd_transactional, mirror = determine_what_to_work_with_local(location_codes=location_codes, id_process=id_process)
    switch_code_local = location_codes.location_mirror_code if  mirror is True  else location_codes.code

    pd_transactional['ds'] = pd_transactional['TRAN_START_DT']
    data_fc = pd_transactional
    data_fc = pd.pivot_table(pd_transactional, values=[
                        'Q_TRX', "CAJERO_EQ"],
                        index=['LOCATION_ID','ds'],
                        aggfunc={'Q_TRX': sum,'CAJERO_EQ': sum})
    data_fc  = pd.DataFrame(data_fc.to_records())
    data_fc[["anio","mes","dia"]]=data_fc.loc[:,("ds")].astype(str).str.split("-", expand=True).astype(int)
    trx1 = data_fc[data_fc['anio'] == int(moment.now().subtract(years=2,months=3).format(fy))]
    trx2 = data_fc[data_fc['anio'] == int(moment.now().format(fy))]

    factor=pd.merge(trx1, trx2, how='outer',  left_on=['LOCATION_ID','mes'], right_on=['LOCATION_ID','mes']).fillna(0)
    factor = calculate_growth_factor(factor=factor)
    apply_factor, month = apply_growth(df=pd_transactional,factor=factor, id_process=id_process, dates_search=dates_search)
    ranges_with_demand_and_factor, blocks_dates, blocks = definition_hourly_ranges_with_demand(apply_factor=apply_factor)
    trx_high_demand_weeks = select_high_demand_week_of_each_month(ranges_with_demand_and_factor=ranges_with_demand_and_factor,month=month)
    hours_preopening_and_postclosing = filter_according_to_preopening_and_postclosing(id_location=switch_code_local)
    brand_skillable_blok = brand_skillable_bloks(blocks_dates=blocks_dates, hours_preopening_and_postclosing=hours_preopening_and_postclosing)
    redefines_demand = redefines_demand_in_skillful_blocks(brand_skillable_bloks=brand_skillable_blok, trx_high_demand_weeks=trx_high_demand_weeks)
    redefines_demand_two = set_min_and_max_igual_two(redefines_demand=redefines_demand, id_location=switch_code_local)
    redefines_demand_two = absenteeism_and_slack(redefines_demand_two=redefines_demand_two)
    result_demand, demand_workers = format_demand(redefines_demand_two=redefines_demand_two)
    formatDemandJson, blocks_horus  = preparad_json(result_demand=result_demand)

    return formatDemandJson, blocks_horus, switch_code_local, mirror