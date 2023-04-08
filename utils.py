import re
import socket
import hashlib


ns = {'x': 'http://www.w3.org/1999/xhtml'}
sep = '=' * 30


def uid(*args):
    md5 = hashlib.md5()
    for arg in args:
        md5.update(arg if isinstance(arg, bytes) else arg.encode('utf-8'))
    return md5.hexdigest()


def trim(text):
    # Remove \xa0 to be compitable with Python2.x
    text = re.sub(u'\u00a0|\u3000', ' ', text)
    return re.sub(r'^\s+|\s+$', '', text)


def is_proxy_availiable(host, port, timeout=1):
    try:
        socket.create_connection((host, int(port)), timeout).close()
    except Exception as e:
        return False
    return True