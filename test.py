# -*- coding: iso-8859-1 -*-
import requests
from bs4 import BeautifulSoup
import time
import re
import sys
import configinfo

session = requests.Session()

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '197',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '_ga=GA1.2.2008092793.1544581836; _gid=GA1.2.345706470.1544581836; _ga=GA1.4.2008092793.1544581836; _gid=GA1.4.345706470.1544581836; GV-tour-complete=1; PHPSESSID=furn9iqkil2i3kf935q5dp3ra6',
    'Host': 'ers.cr.usgs.gov',
    'Origin': 'https://ers.cr.usgs.gov',
    'Referer': 'https://ers.cr.usgs.gov/login/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }
usgs = configinfo.usgs

session.post("https://ers.cr.usgs.gov")
print(session.cookies.get_dict())

ron = requests.get("https://ers.cr.usgs.gov")
cook = ''
for c in ron.cookies:
    cook += c.name +'='+c.value+';'
headers['Cookies'] = cook

r = ron.text
token = re.search(r'<input .*?name="csrf_token".*?value="(.*?)"', r).group(1)
ncforminfo = re.search(r'<input .*?name="__ncforminfo".*?value="(.*?)"', r).group(1)
print(token)
print(ncforminfo)
usgs['csrf_token'] = token
usgs['__ncforminfo'] = ncforminfo
print(usgs)
session.post("https://ers.cr.usgs.gov/login", headers=headers, data=usgs)
print(session.cookies.get_dict())

r = session.get('https://earthexplorer.usgs.gov/download/12864/LC81190322018342LGN00/FR_THERM/EE', stream=True)
# r = session.get('https://earthexplorer.usgs.gov/download/12864/LC81980302013049LGN00/FR_THERM/EE')
# print(r.text)
print(r.status_code)
f = open('test.jpg', 'wb')
for chunk in r.iter_content(chunk_size=1024):
    if chunk:
        f.write(chunk)
f.close()
