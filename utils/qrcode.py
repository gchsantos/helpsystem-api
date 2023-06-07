from django.conf import settings
from qrcode import make
import time


def generate_qr(data, name=str(time.time())):
    img = make(data)
    img_name = f"qr_{name}.png"
    qr_path = f"{settings.QRCODES_ROOT}/{img_name}"
    qr_url = f"{settings.QRCODES_URL}/{img_name}"
    img.save(qr_path)
    return qr_url
