"""必应模块
"""
import os
import re
import urllib
import click
import colorama
import requests
from .cli import xin

colorama.init()

BING_WALLPAPERS_SAVE_PATH = os.path.expanduser(os.path.join('~', 'Pictures', 'BingWallpapers'))
os.makedirs(BING_WALLPAPERS_SAVE_PATH, exist_ok=True)


def bing_wallpapers():
    """必应壁纸数据生成器"""
    session = requests.session()
    for url in ('https://cn.bing.com/HPImageArchive.aspx?format=js&idx=-1&n=7',
                'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=8&n=8',):
        try:
            for image in session.get(url, timeout=(6, 30)).json().get('images', []):
                image_url = urllib.parse.urljoin('https://cn.bing.com', image['url'])  # 图片地址
                image_date = image['enddate']  # 图片日期，格式 YYYYmmdd
                image_title = re.sub(r'(\s*\(©.*?\)\s*$|[【】])', '', image['copyright']).replace('，', '_').strip()  # 图片标题，去除了版权信息等
                image_filename = f'{image_date}-{image_title}.jpg'  # 图片文件名
                yield (image_url, image_filename)
        except BaseException:
            pass


@xin.command()
@click.option('-f', '--force', is_flag=True, help='强制重新下载')
@click.option('-v', '--verbose', is_flag=True, help='输出调试信息')
def download_bing_wallpapers(force, verbose):
    """下载必应壁纸"""
    with click.progressbar(iterable=bing_wallpapers(), length=15, label='下载必应壁纸') as progressbar, \
            requests.session() as session:
        for url, filename in progressbar:
            save_path = os.path.join(BING_WALLPAPERS_SAVE_PATH, filename)
            if not force and os.path.exists(save_path):
                if verbose:
                    click.echo(save_path + click.style(' 已存在', fg='yellow'))
                continue
            try:
                data = session.get(url, timeout=(6, 30)).content
                assert data
            except BaseException:
                if verbose:
                    click.echo(save_path + click.style(' 下载失败', fg='red'))
                continue
            try:
                with open(save_path, 'wb') as output:
                    output.write(data)
            except BaseException:
                if verbose:
                    click.echo(save_path + click.style(' 保存失败', fg='red'))
                continue
            if verbose:
                click.echo(save_path + click.style(' 已下载', fg='green'))
