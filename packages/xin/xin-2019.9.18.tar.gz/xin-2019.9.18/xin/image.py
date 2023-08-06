def is_jpg_data(data):
    return data[:2] == b'\xff\xd8' and data[-2:] == b'\xff\xd9'
