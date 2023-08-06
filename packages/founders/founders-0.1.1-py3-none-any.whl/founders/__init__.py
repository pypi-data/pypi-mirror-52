import requests
import json

from founders import user
from founders import server
from founders import status

current_version = '0.1.1'
newest_version = requests.get('https://pypi.org/pypi/founders/json').json()['info']['version']

if current_version != newest_version:
    print('WARNING: This IS NOT the newest version of founders! Please consider updating to v. {0} you are on v. {1}.'.format(newest_version,current_version))