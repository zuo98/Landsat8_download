import datetime
import math


def connect_earthexplorer_no_proxy(usgs):
    pass


def cycle_day(path):
    """ provides the day in cycle given the path number
    """
    cycle_day_path1 = 5
    cycle_day_increment = 7
    nb_days_after_day1 = cycle_day_path1 + cycle_day_increment * (path - 1)

    cycle_day_path = math.fmod(nb_days_after_day1, 16)
    if path >= 98:  # change date line
        cycle_day_path += 1
    return (cycle_day_path)


def next_overpass(date1, path, sat):
    """ provides the next overpass for path after date1
    """
    date0_L5 = datetime.datetime(1985, 5, 4)
    date0_L7 = datetime.datetime(1999, 1, 11)
    date0_L8 = datetime.datetime(2013, 5, 1)
    if sat == 'LT5':
        date0 = date0_L5
    elif sat == 'LE7':
        date0 = date0_L7
    elif sat == 'LC8':
        date0 = date0_L8
    next_day = math.fmod((date1 - date0).days - cycle_day(path) + 1, 16)
    if next_day != 0:
        date_overpass = date1 + datetime.timedelta(16 - next_day)
    else:
        date_overpass = date1
    return (date_overpass)
