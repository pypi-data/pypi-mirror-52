"""
imagesize 
Simple library to get an image size. 
Support: png, jpg, gif
Returns a tuple (width, height)

get(path)
from_url(url)
"""

import struct
import imghdr
import os
import uuid
import urllib

def test_jpeg(h, f):
    if h[0:4] == '\xff\xd8\xff\xe2' and h[6:17] == b'ICC_PROFILE':
        return 'jpeg'
    if h[0:4] == '\xff\xd8\xff\xee' and h[6:11] == b'Adobe':
        return 'jpeg'
    if h[0:4] == '\xff\xd8\xff\xdb':
        return 'jpeg'
imghdr.tests.append(test_jpeg)

def get(fname):
    '''Determine the image type of fhandle and return its size'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        what = imghdr.what(None, head)
        if what == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif what == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif what == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf or ftype in (0xc4, 0xc8, 0xcc):
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height

def from_url(url):
    """ Get the image size from a URL """
    image_path = ""
    try:
        name = str(uuid.uuid4().hex)
        image_path = "/tmp/%s" % name
        urllib.urlretrieve(url, image_path)
        if os.path.isfile(image_path):
            return get(image_path)
    except Exception as ex:
        logging.exception(ex)
    finally:
        if os.path.isfile(image_path):
            os.remove(image_path)
    return None
