import datetime
import urllib.request
import urllib.parse
import math
import sys
import re
import time
import os
import gzip
import json
import tarfile


def connect_earthexplorer(usgs):
    '''Simulate login
    '''
    cookies = urllib.request.HTTPCookieProcessor()
    opener = urllib.request.build_opener(cookies)
    urllib.request.install_opener(opener)

    data = urllib.request.urlopen(
        "https://ers.cr.usgs.gov").read().decode('utf-8')
    token = re.search(
        r'<input .*?name="csrf_token".*?value="(.*?)"', data).group(1)
    ncforminfo = re.search(
        r'<input .*?name="__ncforminfo".*?value="(.*?)"', data).group(1)

    params = urllib.parse.urlencode(
            dict(
                username=usgs['username'],
                password=usgs['password'],
                csrf_token=token,
                __ncforminfo=ncforminfo)).encode("utf-8")
    request = urllib.request.Request(
        "https://ers.cr.usgs.gov/login", params, headers={})
    f = urllib.request.urlopen(request)

    data = f.read().decode('utf-8')
    f.close()
    if data.find(
            'You must sign in as a registered user to download ' +
            'data or place orders for USGS EROS products'
    ) > 0:
        print("Authentification failed")
        sys.exit(-1)
    print('Login in succeed!')
    return


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def downloadData(dataUrl, path, fielName):
    '''Download data
    '''
    req = urllib.request.urlopen(dataUrl)

    total_size = int(req.info()['Content-Length'].strip())
    downloaded = 0
    CHUNK = 1024 * 1024 * 8
    with open(path+'\\'+fielName, 'wb') as fp:
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


def unZip(fileName):
    g_name = fileName.replace(".gz", "")
    g_file = gzip.GzipFile(fileName)
    open(g_name, "wb+").write(g_file.read())
    g_file.close()

    t_file = tarfile.open(g_name)
    names = t_file.getnames()
    t_name = g_name.replace('.tar', '')
    if os.path.isdir(t_name):
        pass
    else:
        os.mkdir(t_name)
    for name in names:
        t_file.extract(name, t_name)
    t_file.close()


def getJson(fileName):
    '''Convert header files to json files
    '''
    jsondict = {}
    with open(fileName, 'r') as f:
        LINE = f.readline()
        while LINE:
            LINE = str(LINE)
            LINE = LINE.replace('\n', '')
            LINE = LINE.replace(' ', '')
            LINE = LINE.replace('\"', '')
            LINE = LINE.split('=')
            if len(LINE) > 1:
                try:
                    float(LINE[1])
                    jsondict[LINE[0]] = int(LINE[1])
                except:
                    jsondict[LINE[0]] = LINE[1]
            LINE = f.readline()
    jsonfile = json.dumps(jsondict)
    return jsonfile


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


def next_overpass(date1, path):
    """ provides the next overpass for path after date1
    """
    date0 = datetime.datetime(2013, 5, 1)
    next_day = math.fmod((date1 - date0).days - cycle_day(path) + 1, 16)
    if next_day != 0:
        date_overpass = date1 + datetime.timedelta(16 - next_day)
    else:
        date_overpass = date1
    return (date_overpass)
