import qrcode
from pathlib import Path

def make_qr(payload: str, save_to: Path) -> Path:

    img = qrcode.make(payload)
    img.save(save_to)
    return save_to
