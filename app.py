# -*- coding: utf-8 -*-
import datetime
import os
import func
from configinfo import usgs


path_row = '123032'
startTime = '20180912'
endTime = '20180930'
filePath = r'D:\data'

if not os.path.exists(filePath):
    os.makedirs(filePath)

dataStart = datetime.datetime(
    int(startTime[0:4]), int(startTime[4:6]), int(startTime[6:8]))
dataEnd = datetime.datetime(
    int(endTime[0:4]), int(endTime[4:6]), int(endTime[6:8]))
dataPath = path_row[0:3]

dataDate = func.next_overpass(dataStart, int(dataPath))
if dataDate >= dataEnd:
    print('No data for this time period')
else:
    func.connect_earthexplorer(usgs)
    while dataDate < dataEnd:
        dataUrl = 'https://earthexplorer.usgs.gov/download/' + \
            '12864/LC8{}LGN00/STANDARD/EE'.format(
                path_row+dataDate.strftime("%Y%j"))
        fileName = 'LC8_{0}_{1}_LGN00.tar.gz'.format(
            path_row, dataDate.strftime("%Y%m%d"))
        print(fileName)
        func.downloadData(dataUrl, filePath, fileName)
        func.unZip(filePath+'\\'+fileName)
        os.remove(filePath+'\\'+fileName)
        os.remove(filePath+'\\'+fileName.split('.')[0]+'.tar')

        dataDate = dataDate+datetime.timedelta(16)

print('\n Data download completed')
