import pandas as pd
import calendar
import moment
from app.generate.entities.last_month import ElastMonth 
from datetime import date, datetime, time
from dateutil import relativedelta as rdelta

ff = 'YYYY-MM-DD'
ff_hh = 'YYYY-MM-DD HH:mm:ss'
fy = 'YYYY'
fm = 'MM'
fd = 'DD'
INFO = 'INFORMATION'
ERR  = 'ERROR'
WAR = 'WARNING'
mesagges = {
    'pross_scheduling': 'Procesando agenda',
    'pross_trass':'Generando Dataframe con los datos transaccionales',
    'df_null':'no se encontraron datos del local en la tabla FC_TRX_LINEALS',
    'df_transaccionales':'Se encontraron datos transaccionales',
    'ff_cal_fc':'start: {}, end: {} -> Filtro factor de crecimiento [dates_filter_growth_factor]',
    'ff_filter_months':'start: {}, end: {} -> aplicar factor de crecimiento [apply_growth]',
    'month_to_month':'start: {}, end: {} -> generar input mes a mes',
    'location_mirror': 'Inicia operación con local espejo por no encontrar datos transaccionales. {}'
}
moment.now().locale('America/Santiago').timezone('America/Santiago')

current_year = int(moment.now().format(fy))
current_month = int(moment.now().format(fm))
today_day = int(moment.now().format(fd))
now_ff_hh = moment.now().format(ff_hh)
now_ff = moment.now().format(ff)
last_month_day = calendar.monthrange(current_year, current_month)[1]
monthyear = int("{}{}".format(moment.now().\
    format(fy),moment.now().format(fm)))

## previous moment info
previous_current_year = int(moment.now().\
    subtract(months=1).format(fy))

previous_current_month = int(moment.now().\
    subtract(months=1).format(fm))

previous_last_month_day = calendar.\
    monthrange(previous_current_year, previous_current_month)[1]

previous_start_month_ff = moment.now().\
    subtract(months=1).replace(day=1).format(ff)

previous_end_month_ff = moment.now().\
    subtract(months=1).\
        replace(day=previous_last_month_day).format(ff)

previous_end_month = moment.now().\
    subtract(months=1).\
        replace(day=previous_last_month_day)

previous_monthyear = int("{}{}".format(moment.now().\
    subtract(months=1).format(fy), moment.now().\
        subtract(months=1).format(fm)))

## FIN previous moment

def determinate_previous_start_month_ff(annual: bool, lastMonth: ElastMonth = None):
    if annual is True:
        start = moment.now().\
            subtract(years=2, months=1).\
                replace(day=1)
    else:
        start = moment.date(lastMonth.date_month_end).\
            add(months=1).\
                replace(day=1)

    date_start = date(int(start.format(fy)),int(start.format(fm)),int(start.format(fd)))
    date_end = date(int(previous_end_month.format(fy)),int(previous_end_month.format(fm)),int(previous_end_month.format(fd)))
    diff = rdelta.relativedelta(date_end, date_start)

    if int("{0.years}".format(diff)) == 1:
        months = 13
    elif int("{0.months}".format(diff)) == 0:
        months = 1
    else:
        months = int("{0.months}".format(diff))

    return {'start':start.format(ff),'end':previous_end_month_ff,'months':months}

def determinate_previous_scheduling(attemps: int):
    return moment.now().\
        subtract(months=1).\
            replace(day=attemps).format(ff)

def today_ff_add_days(day=int):
    return moment.now().add(days=day).format(ff)

def incremet_month(date: str,num_month: int):

    start = moment.date(date).\
        add(months=num_month).\
            replace(day=1).format(ff)

    last_month_day = calendar.monthrange(int(moment.date(start).format(fy)),int(moment.date(start).format(fm)))[1]

    end = moment.date(start).\
        replace(day=last_month_day).format(ff)

    return {'start':start,'end':end,'months':1}

def fn_now_ff_hh():
    return moment.now().format(ff_hh)

def correct_demand(data: tuple= []):
    week = {}
    dates = []
    for x in data:
        week[datetime.strptime(x[0], '%Y-%m-%d').isoweekday()] = x[0]
        num_datos = (len(x) - 1)
    for day_week in range (1, 8):
        aggregate = []
        if day_week not in week:
            if day_week > 1:
                date = moment.date(week.get(1)).add(days=(day_week - 1)).format(ff)
            else:
                keys_id = list(week.keys())
                date = moment.date(week.get(keys_id[0])).subtract(days=(keys_id[0] - 1)).format(ff)
                week[datetime.strptime(date, '%Y-%m-%d').isoweekday()] = date
            aggregate.append(date)
            for n in range(0,num_datos):
                aggregate.append(0)
            data.append(aggregate)
            dates.append([date,day_week - 1])
        else:
            dates.append([week.get(day_week),day_week - 1])

    return sorted(data), dates

def corrige_post(tb):
    post = tb.POST_CLOSE_TIME
    if post <= 30:
        return 0
    elif post > 30:
        return 30

def inicio_lun_dia1(tb):
    i_lun = pd.to_datetime(tb.i_MON, format="%H:%M:%S")
    f_lun = pd.to_datetime(tb.f_MON, format="%H:%M:%S")
    if f_lun < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return i_lun
    elif f_lun > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return i_lun

def fin_lun_dia1(tb):
    i_lun = pd.to_datetime(tb.i_MON, format="%H:%M:%S")
    f_lun = pd.to_datetime(tb.f_MON, format="%H:%M:%S")
    if f_lun < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return pd.to_datetime('23:30:00', format="%H:%M:%S")
    elif f_lun > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return f_lun

def inicio_lun_dia2(tb):
    i_lun = pd.to_datetime(tb.i_MON, format="%H:%M:%S")
    f_lun = pd.to_datetime(tb.f_MON, format="%H:%M:%S")
    if f_lun < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return pd.to_datetime('00:00:00', format="%H:%M:%S")
    elif f_lun > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return None

def fin_lun_dia2(tb):
    i_lun = pd.to_datetime(tb.i_MON, format="%H:%M:%S")
    f_lun = pd.to_datetime(tb.f_MON, format="%H:%M:%S")
    if f_lun < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return f_lun
    elif f_lun > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return None

def inicio_mar_dia1(tb):
    i_mar = pd.to_datetime(tb.i_TUE, format="%H:%M:%S")
    f_mar = pd.to_datetime(tb.f_TUE, format="%H:%M:%S")
    if f_mar < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return i_mar
    elif f_mar > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return i_mar;

def fin_mar_dia1(tb):
    i_mar = pd.to_datetime(tb.i_TUE, format="%H:%M:%S")
    f_mar = pd.to_datetime(tb.f_TUE, format="%H:%M:%S")
    if f_mar < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return pd.to_datetime('23:30:00', format="%H:%M:%S")
    elif f_mar > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return f_mar;

def inicio_mar_dia2(tb):
    i_mar = pd.to_datetime(tb.i_TUE, format="%H:%M:%S")
    f_mar = pd.to_datetime(tb.f_TUE, format="%H:%M:%S")
    if f_mar < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return pd.to_datetime('00:00:00', format="%H:%M:%S")
    elif f_mar > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return None;

def fin_mar_dia2(tb):
    i_mar = pd.to_datetime(tb.i_TUE, format="%H:%M:%S")
    f_mar = pd.to_datetime(tb.f_TUE, format="%H:%M:%S")
    if f_mar < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return f_mar
    elif f_mar > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return None;

def inicio_mie_dia1(tb):
    i_mie = pd.to_datetime(tb.i_WED, format="%H:%M:%S")
    f_mie = pd.to_datetime(tb.f_WED, format="%H:%M:%S")
    if f_mie < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return i_mie
    elif f_mie > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return i_mie

def fin_mie_dia1(tb):
    i_mie = pd.to_datetime(tb.i_WED, format="%H:%M:%S")
    f_mie = pd.to_datetime(tb.f_WED, format="%H:%M:%S")
    if f_mie < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return pd.to_datetime('23:30:00', format="%H:%M:%S")
    elif f_mie > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return f_mie

def inicio_mie_dia2(tb):
    i_mie = pd.to_datetime(tb.i_WED, format="%H:%M:%S")
    f_mie = pd.to_datetime(tb.f_WED, format="%H:%M:%S")
    if f_mie < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return pd.to_datetime('00:00:00', format="%H:%M:%S")
    elif f_mie > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return None

def fin_mie_dia2(tb):
    i_mie = pd.to_datetime(tb.i_WED, format="%H:%M:%S")
    f_mie = pd.to_datetime(tb.f_WED, format="%H:%M:%S")
    if f_mie < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return f_mie
    elif f_mie > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return None

def inicio_jue_dia1(tb):
    i_jue = pd.to_datetime(tb.i_THU, format="%H:%M:%S")
    f_jue = pd.to_datetime(tb.f_THU, format="%H:%M:%S")
    if f_jue < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return i_jue
    elif f_jue > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return i_jue

def fin_jue_dia1(tb):
    i_jue = pd.to_datetime(tb.i_THU, format="%H:%M:%S")
    f_jue = pd.to_datetime(tb.f_THU, format="%H:%M:%S")
    if f_jue < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return pd.to_datetime('23:30:00', format="%H:%M:%S")
    elif f_jue > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return f_jue

def inicio_jue_dia2(tb):
    i_jue = pd.to_datetime(tb.i_THU, format="%H:%M:%S")
    f_jue = pd.to_datetime(tb.f_THU, format="%H:%M:%S")
    if f_jue < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return pd.to_datetime('00:00:00', format="%H:%M:%S")
    elif f_jue > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return None

def fin_jue_dia2(tb):
    i_jue = pd.to_datetime(tb.i_THU, format="%H:%M:%S")
    f_jue = pd.to_datetime(tb.f_THU, format="%H:%M:%S")
    if f_jue < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return f_jue
    elif f_jue > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return None

def inicio_vie_dia1(tb):
    i_vie = pd.to_datetime(tb.i_FRI, format="%H:%M:%S")
    f_vie = pd.to_datetime(tb.f_FRI, format="%H:%M:%S")
    if f_vie < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return i_vie
    elif f_vie > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return i_vie

def fin_vie_dia1(tb):
    i_vie = pd.to_datetime(tb.i_FRI, format="%H:%M:%S")
    f_vie = pd.to_datetime(tb.f_FRI, format="%H:%M:%S")
    if f_vie < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return pd.to_datetime('23:30:00', format="%H:%M:%S")
    elif f_vie > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return f_vie

def inicio_vie_dia2(tb):
    i_vie = pd.to_datetime(tb.i_FRI, format="%H:%M:%S")
    f_vie = pd.to_datetime(tb.f_FRI, format="%H:%M:%S")
    if f_vie < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return pd.to_datetime('00:00:00', format="%H:%M:%S")
    elif f_vie > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return None

def fin_vie_dia2(tb):
    i_vie = pd.to_datetime(tb.i_FRI, format="%H:%M:%S")
    f_vie = pd.to_datetime(tb.f_FRI, format="%H:%M:%S")
    if f_vie < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return f_vie
    elif f_vie > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return None

def inicio_sab_dia1(tb):
    i_sab = pd.to_datetime(tb.i_SAT, format="%H:%M:%S")
    f_sab = pd.to_datetime(tb.f_SAT, format="%H:%M:%S")
    if f_sab < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return i_sab
    elif f_sab > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return i_sab

def fin_sab_dia1(tb):
    i_sab = pd.to_datetime(tb.i_SAT, format="%H:%M:%S")
    f_sab = pd.to_datetime(tb.f_SAT, format="%H:%M:%S")
    if f_sab < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return pd.to_datetime('23:30:00', format="%H:%M:%S")
    elif f_sab > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return f_sab

def inicio_sab_dia2(tb):
    i_sab = pd.to_datetime(tb.i_SAT, format="%H:%M:%S")
    f_sab = pd.to_datetime(tb.f_SAT, format="%H:%M:%S")
    if f_sab < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return pd.to_datetime('00:00:00', format="%H:%M:%S")
    elif f_sab > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return None

def fin_sab_dia2(tb):
    i_sab = pd.to_datetime(tb.i_SAT, format="%H:%M:%S")
    f_sab = pd.to_datetime(tb.f_SAT, format="%H:%M:%S")
    if f_sab < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return f_sab
    elif f_sab > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return None

def inicio_dom_dia1(tb):
    i_dom = pd.to_datetime(tb.i_SUN, format="%H:%M:%S")
    f_dom = pd.to_datetime(tb.f_SUN, format="%H:%M:%S")
    if f_dom < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return i_dom
    elif f_dom > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return i_dom

def fin_dom_dia1(tb):
    i_dom = pd.to_datetime(tb.i_SUN, format="%H:%M:%S")
    f_dom = pd.to_datetime(tb.f_SUN, format="%H:%M:%S")
    if f_dom < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return pd.to_datetime('23:30:00', format="%H:%M:%S")
    elif f_dom > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return f_dom

def inicio_dom_dia2(tb):
    i_dom = pd.to_datetime(tb.i_SUN, format="%H:%M:%S")
    f_dom = pd.to_datetime(tb.f_SUN, format="%H:%M:%S")
    if f_dom < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return pd.to_datetime('00:00:00', format="%H:%M:%S")
    elif f_dom > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return None

def fin_dom_dia2(tb):
    i_dom = pd.to_datetime(tb.i_SUN, format="%H:%M:%S")
    f_dom = pd.to_datetime(tb.f_SUN, format="%H:%M:%S")
    if f_dom < pd.to_datetime('06:00:00', format="%H:%M:%S"):
        return f_dom
    elif f_dom > pd.to_datetime("06:00:00", format="%H:%M:%S"):
        return None

def corrige_d(tb):
    d= tb.diasem
    h = tb.HORA_fmto
    i_lun_d1 = tb.i_lun_d1
    f_lun_d1 = tb.f_lun_d1
    i_lun_d2 = tb.i_lun_d2
    f_lun_d2 = tb.f_lun_d2

    i_mar_d1 = tb.i_mar_d1
    f_mar_d1 = tb.f_mar_d1
    i_mar_d2 = tb.i_mar_d2
    f_mar_d2 = tb.f_mar_d2

    i_mie_d1 = tb.i_mie_d1
    f_mie_d1 = tb.f_mie_d1
    i_mie_d2 = tb.i_mie_d2
    f_mie_d2 = tb.f_mie_d2

    i_jue_d1 = tb.i_jue_d1
    f_jue_d1 = tb.f_jue_d1
    i_jue_d2 = tb.i_jue_d2
    f_jue_d2 = tb.f_jue_d2

    i_vie_d1 = tb.i_vie_d1
    f_vie_d1 = tb.f_vie_d1
    i_vie_d2 = tb.i_vie_d2
    f_vie_d2 = tb.f_vie_d2

    i_sab_d1 = tb.i_sab_d1
    f_sab_d1 = tb.f_sab_d1
    i_sab_d2 = tb.i_sab_d2
    f_sab_d2 = tb.f_sab_d2

    i_dom_d1 = tb.i_dom_d1
    f_dom_d1 = tb.f_dom_d1
    i_dom_d2 = tb.i_dom_d2
    f_dom_d2 = tb.f_dom_d2

    if d== 0 and i_lun_d2 == None:
        if (i_lun_d1 <= h <= f_lun_d1):
            return 1;
    elif d== 0 and i_lun_d2 != None:
        if ((i_lun_d1 <= h <= f_lun_d1) or (i_lun_d2 <= h <= f_lun_d2)):
            return 1;

    if d== 1 and i_mar_d2 == None:
        if (i_mar_d1 <= h <= f_mar_d1):
            return 1;
    elif d== 1 and i_mar_d2 != None:
        if ((i_mar_d1 <= h <= f_mar_d1) or (i_mar_d2 <= h <= f_mar_d2)):
            return 1;

    if d== 2 and i_mie_d2 == None:
        if (i_mie_d1 <= h <= f_mie_d1):
            return 1;
    elif d== 2 and i_mie_d2 != None:
        if ((i_mie_d1 <= h <= f_mie_d1) or (i_mie_d2 <= h <= f_mie_d2)):
            return 1;

    if d== 3 and i_jue_d2 == None:
        if (i_jue_d1 <= h <= f_jue_d1):
            return 1;
    elif d== 3 and i_jue_d2 != None:
        if ((i_jue_d1 <= h <= f_jue_d1) or (i_jue_d2 <= h <= f_jue_d2)):
            return 1;

    if d== 4 and i_vie_d2 == None:
        if (i_vie_d1 <= h <= f_vie_d1):
            return 1;
    elif d== 4 and i_vie_d2 != None:
        if ((i_vie_d1 <= h <= f_vie_d1) or (i_vie_d2 <= h <= f_vie_d2)):
            return 1;

    if d== 5 and i_sab_d2 == None:
        if (i_sab_d1 <= h <= f_sab_d1):
            return 1;
    elif d== 5 and i_sab_d2 != None:
        if ((i_sab_d1 <= h <= f_sab_d1) or (i_sab_d2 <= h <= f_sab_d2)):
            return 1;

    if d== 6 and i_dom_d2 == None:
        if (i_dom_d1 <= h <= f_dom_d1):
            return 1;
    elif d== 6 and i_dom_d2 != None:
        if ((i_dom_d1 <= h <= f_dom_d1) or (i_dom_d2 <= h <= f_dom_d2)):
            return 1;

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        res = check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        res = check_time >= begin_time or check_time <= end_time
    return 1 if res is True else 0

def validate_range(df:object):
    existe = (df
                .apply(lambda hora: is_time_between(hora['start'], hora['end'],time(int(hora['hora'][0:1]),int(hora['hora'][2:4]))) if hora['hora'][1:2] == ':' else is_time_between(hora['start'], hora['end'],time(int(hora['hora'][0:2]),int(hora['hora'][3:5]))), axis=1)
             )
    df['existe'] = existe
    return df