import datetime

def dt(date_time):
    return str(date_time)[8:10] + str(date_time)[5:7] + str(date_time)[:4] + "_" + str(date_time)[11:13] + str(date_time)[14:16] + str(date_time)[17:19]