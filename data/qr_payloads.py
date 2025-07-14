import random


QR_PAYLOADS = {
    "distrA": {
        "text": f"https://public.test.onlinebank.kz/applink/b2b/distributor/181040020686/client/720310301370/invoiceId/{random.randint(10**10, 10**11 - 1)}/amount/1/invoiceTitle/",
        "file_name": "Universal.png"
    },
    "distrB": {
        "text": f"https://homebank.kz/payments/megapolisKZ?contract={random.randint(10**10, 10**11 - 1)}&iin=720310301370&amount=1",
        "file_name": "Megapolis.png"
    },
    # добавите нового дистрибьютора — просто допишите словарь
}
