# -*- coding: utf-8 -*-
import os, sys, math, urllib.request, urllib.parse, time, math, shutil
import subprocess
import optparse
import csv
import re
from configinfo import usgs

cookies = urllib.request.HTTPCookieProcessor()
opener = urllib.request.build_opener(cookies)
urllib.request.install_opener(opener)

data = urllib.request.urlopen("https://ers.cr.usgs.gov").read().decode('utf-8')
token = re.search(r'<input .*?name="csrf_token".*?value="(.*?)"', data).group(1)
ncforminfo = re.search(r'<input .*?name="__ncforminfo".*?value="(.*?)"', data).group(1)


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


params = urllib.parse.urlencode(
        dict(
            username=usgs['username'],
            password=usgs['password'],
            csrf_token=token,
            __ncforminfo=ncforminfo)).encode("utf-8")

print(params)

request = urllib.request.Request(
    "https://ers.cr.usgs.gov/login", params, headers={})
f = urllib.request.urlopen(request)

req = urllib.request.urlopen(
    'https://earthexplorer.usgs.gov/download/12864/LC81230322018338LGN00/STANDARD/EE')

info = req.info()['Content-Type']
print(info)
total_size = int(req.info()['Content-Length'].strip())

downloaded = 0
CHUNK = 1024 * 1024 * 8
with open('123.zip', 'wb') as fp:
    start = time.time()
    while True:
        chunk = req.read(CHUNK)
        downloaded += len(chunk)
        done = int(50 * downloaded / total_size)
        sys.stdout.write('\r[{1}{2}]{0:3.0f}% {3}ps'.format(
            math.floor((float(downloaded) / total_size) * 100),
            '=' * done, ' ' * (50 - done),
            sizeof_fmt((downloaded // int((time.time() - start))) / 8)))
        sys.stdout.flush()
        if not chunk:
            break
        fp.write(chunk)
