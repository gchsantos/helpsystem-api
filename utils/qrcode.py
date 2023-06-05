from django.conf import settings
from qrcode import make
import time


def generate_qr(data, name=str(time.time())):
    img = make(data)
    img_name = f"qr_{name}.png"
    img.save(f"{settings.QRCODES_ROOT}/{img_name}")
    return True
