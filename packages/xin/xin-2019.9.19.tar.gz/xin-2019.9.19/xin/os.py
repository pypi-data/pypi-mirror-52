"""os module for python-xin package
"""

from os.path import expanduser
import platform

USER_HOME_PATH = expanduser('~')
SYSTEM = platform.system()


def mkdirs(path):
    import os
    abspath = os.path.abspath(path)
    os.makedirs(abspath, exist_ok=True)
    return abspath


def save_file(path, data=None, url=None, overwirte=False, **kwargs):
    import os
    import requests
    if os.path.exists(path) and not overwirte:
        return 'file exists'
    try:
        data = data or requests.get(url, **kwargs).content
        assert data, 'empty data'
        directory = os.path.dirname(path)
        mkdirs(directory)
        with open(path, 'wb') as output:
            output.write(data)
    except BaseException as error:
        return error


for _ in [expanduser, platform]:
    del _
