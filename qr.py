

def QR(data):# Importing library
    import qrcode
    obj_qr = qrcode.QRCode(  
    version = 1,  
    error_correction = qrcode.constants.ERROR_CORRECT_L,  
    box_size = 10,  
    border = 0.1)
    obj_qr.add_data(data)  
    obj_qr.make(fit = True)  
    qr_img = obj_qr.make_image(back_color=(255, 255, 255), fill_color=(200, 0, 0))  
    qr_img.save("./assets/img/qr.png")   