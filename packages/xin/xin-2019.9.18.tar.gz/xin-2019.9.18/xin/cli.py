"""命令行模块
"""
import click


@click.group()
@click.option('-c', '--clear', is_flag=True, help='运行前清除屏幕')
def xin(clear):
    if clear:
        click.clear()
