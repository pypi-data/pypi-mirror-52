"""HTTP module for xin Python Library
"""

import os
import datetime
import requests


def public_ip_address(**kwargs):
    """Get the public IP address (using httpbin.org's IP API)

    Args:
        **kwargs: Arbitrary keyword arguments.

    Return:
        The requester's public IP Address or '' (if anything was worng)
    """
    try:
        kwargs['timeout'] = kwargs.pop('timeout', 30)
        response = requests.get('http://httpbin.org/ip', **kwargs)
        _public_ip_address, *_ = response.json().get('origin', '').split(',')
        return _public_ip_address
    except BaseException as error:
        print('ERROR:', error)
        return ''


def dynu_ip_update(username='', password='', myip='', **kwargs) -> bool:
    """Update the primary IP address for your Dynu domain name

    Args:
        username: Your Dynu username.
        password: Your Dynu password.
        myip: Your public IP address. Will be auto detected if not given.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        The return value. True for success, False otherwise.
    """
    now = datetime.datetime.now().strftime(f'%F %T')
    username = username or os.environ.get('DYNU_USERNAME')
    password = password or os.environ.get('DYNU_PASSWORD')
    myip = myip or public_ip_address(timeout=30)
    params = {'username': username, 'password': password, 'myip': myip}
    url = 'http://api.dynu.com:8245/nic/update'
    kwargs['timeout'] = kwargs.pop('timeout', 30)
    kwargs['proxies'] = kwargs.pop(
        'proxies', {'http': 'http://127.0.0.1:8118'}
    )
    try:
        assert username and password and myip, 'short of arguments!'
        response = requests.get(url=url, params=params, **kwargs)
        assert response.text.startswith(
            'good') or response.text.startswith('nochg'), response.text
        print(f'{now} SUCESS: {response.text} ({myip})')
        return True
    except BaseException as error:
        print(f'{now} ERROR: {error}')
        return False


def ip_address_info(ip='') -> dict:
    """Get IP address information

    Args:
        ip: IP address.

    Returns:
        IP address information as a dict:
        {
            'ip': '58.212.210.33',
            'city': 'Nanjing',
            'region': 'Jiangsu',
            'region_code': 'JS',
            'country': 'CN',
            'country_name': 'China',
            'continent_code': 'AS',
            'in_eu': False,
            'postal': None,
            'latitude': 32.0617,
            'longitude': 118.7778,
            'timezone': 'Asia/Shanghai',
            'utc_offset': '+0800',
            'country_calling_code': '+86',
            'currency': 'CNY',
            'languages': 'zh-CN,yue,wuu,dta,ug,za',
            'asn': 'AS4134',
            'org': 'No.31,Jin-rong Street'
        }
    """
    ip = ip or public_ip_address()
    response = requests.get(f'https://ipapi.co/{ip}/json', timeout=30)
    return response.json()


def is_online() -> bool:
    """Check if internet connection is OK

    Return:
        True for OK, False otherwise.
    """
    return any((requests.head(url, timeout=3.0).status_code == 200
                for url in ('http://www.163.com',
                            'http://www.baidu.com',
                            'http://www.sina.com.cn')))
