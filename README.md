# Landsat8_download

## Description

- Programming Language : **python 3**

- I want to automatically download Landsat8 data. [Olivier Hagolle](https://github.com/olivierhagolle) has done this with python2, but I need to use python3, so I made some changes based on [Olivier Hagolle's project](https://github.com/olivierhagolle/LANDSAT-Download).

## Examples

- First you need to create a new configinfo.py file and create a dictionary called usgs to record your account password, for example: usgs={username: AAA, password:AAAA}

- Then modify the three variables in app.py. For example :

```python
    path_row = '123032'
    startTime = '20180912'
    endTime = '20180930'
```

- Last run the app.py.