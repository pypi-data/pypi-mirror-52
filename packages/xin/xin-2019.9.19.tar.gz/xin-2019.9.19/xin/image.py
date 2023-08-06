"""image module for python-xin package
"""


def is_jpg_data(data: bytes) -> bool:
    """判断数据是否是JPG文件数据"""
    return data[:2] == b'\xff\xd8' and data[-2:] == b'\xff\xd9'
