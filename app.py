# -*- coding: utf-8 -*-
# Landsat Data download from earth explorer

import os, sys, math, requests, time, math, shutil
import subprocess
import optparse
import datetime
import csv
import re
import func
output = r'C:\Users\STUDENT\Desktop'
#    [option, bird, start_date, scene, ]
key = ['scene', 'LC8', '20130127', '198030']

usgs = configinfo.usgs
produit = key[1]
path = key[3][0:3]
row = key[3][3:6]

year_start = int(key[2][0:4])
month_start = int(key[2][4:6])
day_start = int(key[2][6:8])
date_start = datetime.datetime(year_start, month_start, day_start)
date_end = datetime.datetime.now()
print(date_start)
global downloaded_ids
downloaded_ids = []
func.connect_earthexplorer_no_proxy(usgs)
if produit == 'LC8':
    repert = '12864'
    stations = ['LGN']

curr_date = func.next_overpass(date_start, int(path), produit)

check = 1
# while (curr_date < date_end) and check == 1:
date_asc = curr_date.strftime("%Y%j")
notfound = False
print('Searching for images on (julian date): ' + date_asc + '...')
curr_date = curr_date + datetime.timedelta(16)
for station in stations:
    for version in ['00', '01', '02']:
        nom_prod = produit + key[3] + date_asc + station + version
        tgzfile = os.path.join(output, nom_prod + '.tgz')
        lsdestdir = os.path.join(output, nom_prod)
        url = "https://earthexplorer.usgs.gov/download/%s/%s/STANDARD/EE" % (
            repert, nom_prod)
        print(url)
