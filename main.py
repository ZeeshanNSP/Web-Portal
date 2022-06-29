from ast import Load
import json
from re import L
from socket import timeout
import sys
import time
from datetime import datetime
import os
import pymongo
from flask import Flask, render_template,redirect,request,jsonify,session,abort,send_from_directory
from flask_cors import CORS
import random as r
from numerize import numerize

app = Flask(__name__)
CORS(app)

#configuration variables
app.secret_key = "53C437"
USERS = None
TITLE = "NSP"
# Methods and operation for the session and other utilities
def sessionCheck():
    if "user" in session:
        return True
    else:
        return False
def LoadUsers():
    f = open("cred.json","r")
    global USERS
    USERS = json.load(f)
    f.close()


def updateCred():
    f = open("cred.json","w")
    f.write(json.dumps(USERS))
    f.close()


def currentUser():
    if sessionCheck():
        u = session["user"]
        return USERS[u]  

#routes for the web portal   
# 
#  
@app.route("/getBandwidth")
def getBd():
    tx = r.randint(9,10000)
    rx = r.randint(9,10000)
    return {"tx":tx,"rx":rx}
@app.route("/logout",methods = ["GET"])
def Logout():
    session.pop("user")
    return redirect("/")     


@app.route("/profile",methods=["GET","POST"])
def profile():
    if sessionCheck():
        if request.method =="GET":
            return render_template("profile.html",title = TITLE,user = currentUser(),noti = None)
        else:
            return  render_template("profile.html",title= TITLE,user = currentUser(),noti = "Updated Successfully")
    else:
        return redirect("/")
@app.route("/",methods = ["GET","POST"])
def index():
    if request.method == "GET":
        if sessionCheck():
            return render_template("index.html",title=TITLE,clients = numerize.numerize(50000),sess=numerize.numerize(1024),act_voucher=numerize.numerize(5200),vouchers=numerize.numerize(6000))
        else:
            return render_template("login.html",title = TITLE)
    if request.method == "POST":
        user = request.form.get("user")
        pswd = request.form.get("password")
        if user in USERS:
            if USERS[user]["password"] == pswd:
                session["user"] = user
                return "Logging you In"
            else:
                return "Invalid Credentials"
        else:
            return "Username Invalid"        
        

#Routes for the css,js and other image assets
@app.route("/assets/<path:path>")
def sendAssets(path):
    return send_from_directory("assets/",path)
@app.route("/css/<path:path>")
def sendCss(path):
    return send_from_directory("css/",path)
@app.route("/vendors/<path:path>")
def sendVendor(path):
    return send_from_directory("vendors/",path)
@app.route("/js/<path:path>")
def sendJS(path):
    return send_from_directory("js/",path)

if __name__ == "__main__":
    LoadUsers()
    app.debug = True
    app.run(host="0.0.0.0",port=443, use_reloader=True,ssl_context=("localhost+2.pem","localhost+2-key.pem"))