from hashlib import sha1
from io import BytesIO

import qrcode
from qrcode.constants import ERROR_CORRECT_H


def make_qrcode(message):
    qr = qrcode.QRCode(version=3, error_correction=ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(message)
    img = BytesIO()
    qr.make_image().save(img, 'JPEG')
    img.name = 'qr-' + sha1(message.encode()).hexdigest() + '.jpg'
    img.seek(0)
    return img
