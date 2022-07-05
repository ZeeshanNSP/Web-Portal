

def getShortURL(url):
    import requests
    api_key = "672811c1f95e820df4623207537d289632358"
    api_url = f"https://cutt.ly/api/api.php?key={api_key}&short={url}"
    data = requests.get(api_url).json()["url"]
    if data["status"] == 7:
        return data["shortLink"]
    else:
        return url

def QR(data):# Importing library
    import qrcode
    obj_qr = qrcode.QRCode(  
    version = 1,  
    error_correction = qrcode.constants.ERROR_CORRECT_L,  
    box_size = 10,  
    border = 0.1)
    data = getShortURL(data)
    obj_qr.add_data(data)  
    obj_qr.make(fit = True)  
    qr_img = obj_qr.make_image(back_color=(255, 255, 255), fill_color=(200, 0, 0))  
    qr_img.save("./assets/img/qr.png")   