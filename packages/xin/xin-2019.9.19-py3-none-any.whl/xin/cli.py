"""cli module for python-xin package
"""

import click
from . import net


@click.group()
@click.option('-c', '--clear', is_flag=True, help='运行前清除屏幕')
def xin(clear):
    """命令组"""
    if clear:
        click.clear()


@xin.command()
@click.argument('ip', default='')
@click.option('-i', '--info', is_flag=True, help='查询自己IP的信息')
def ip(ip, info):
    """查询IP相关信息"""
    if ip or info:
        data = net.ip_address_info(ip)
        click.echo('''
ip:         {ip}
continent:  {continent_code}
country:    {country_name}
region:     {region}
city:       {city}
timezone:   {timezone}
utc-offset: {utc_offset}
latitude:   {latitude}
longitude:  {longitude}
asn:        {asn}
org:        {org}'''.format(**data))
    else:
        click.echo(net.public_ip_address())
