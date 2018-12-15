import os


def qr_callback(uuid,status,qrcode):
    path_url = os.path.join(os.getcwd(),'qrcode')
    with open(os.path.join(path_url,'{}.png'.format(uuid)),'wb') as qr_code:
        qr_code.write(qrcode)


