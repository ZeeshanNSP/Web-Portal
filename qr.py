

def QR(data):# Importing library
    import qrcode
    img = qrcode.make(data)
    img.save('./assets/img/qr.png')
