import json
import sys
import time
from datetime import datetime, timedelta,date
import os
from tracemalloc import start
import pymongo
from flask import Flask, render_template,redirect,request,jsonify,session,abort,send_from_directory
from flask_cors import CORS
import random as r
from numerize import numerize
from rg import ReceiptGenerator
from vg import VoucherGenerator
import string
from pdf import createPdf as pdf

app = Flask(__name__)
CORS(app)

#database connection and collections
DBURL = "mongodb+srv://testUser:testUser@nv9-testing.9azuqdw.mongodb.net/?retryWrites=true&w=majority"
myclient = pymongo.MongoClient(DBURL)
mydb = myclient["NV9-Testing"]
users = mydb["users"]
transactions = mydb["transactions"]
logs = mydb["log"]
terminals = mydb["terminal"]
STACKER_LIMIT = 510
#configuration variables
app.secret_key = "53C437"
USERS = None
TITLE = "NSP"
# Methods and operation for the session and other utilities
def sessionCheck():
    try:
        if "user" in session:
            return True
        else:
            return False
    except:
        return False
def getCurrentTimeStampClean():
    from datetime import date
    now = datetime.now()
    d1 =  now.strftime("%d%m%Y%H%M%S")
    return str(d1)
def getCurrentDate():
    from datetime import date
    now = datetime.now()
    d1 =  now.strftime("%d/%m/%Y")
    return str(d1)
def getCurrentTimeStamp():
    from datetime import date
    now = datetime.now()
    d1 =  now.strftime("%d/%m/%Y %H:%M:%S")
    return str(d1)
def LoadUsers():
    f = open("cred.json","r")
    global USERS
    USERS = json.load(f)
    f.close()

def getTerminals(query={}):
    t = terminals.find(query)
    res = []
    for i in t:
        res.append(i)
    return res

def getSites():
    return []
def getSiteById(id):
    return {"code":id,"name":id,"address":id}

def updateCred():
    f = open("cred.json","w")
    f.write(json.dumps(USERS,indent=4))
    f.close()

def getLogs(query={}):
    r = logs.find(query)
    res = []
    for i in r:
        res.append(i)
    return res

def getTransactions(query={}):
    r = transactions.find(query)
    res = []
    for i in r:
        if "pin" not in i:
            res.append(i)
    return res

def getVouchers(query={}):
    r = transactions.find({})
    res = []
    for i in r:
        if "pin" in i:
            res.append(i)
    return res
def getClients(query={}):
    r = users.find(query)
    res = []
    for i in r:
        res.append(i)
    return res
def currentUser():
    if sessionCheck():
        u = session["user"]
        return USERS[u]  

def getUsers():
    res = []
    u = currentUser()
    for i in USERS:
        if not (i == u['username']):
            res.append(USERS[i])
    return res

def date_range(start, end):
    delta = end - start  
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days
def getDatefromString(s):
    s = s.split("/")
    date_time_obj = date(int(s[2]),int(s[1]),int(s[0]))
    return date_time_obj
#routes for the web portal   
# 
# 
# 
#  
@app.route("/terminal/<id>",methods=["GET","POST"])
def terminalDetail(id):
    if sessionCheck():
        if request.method =="GET":
            t = getTerminals({"TID":{"$eq":id}})[0]
            rem = t['config']['counter']
            tt = 0
            for i in rem:
                tt = tt+ rem[i]
            return render_template("terminalDetail.html",title=TITLE,user = currentUser(),noti = None,terminal = t,remaining_space= STACKER_LIMIT -tt,logs=getLogs())
        elif request.method == "POST":
            st = request.form.get("status")
            if st is None:
                query = { "TID": {"$eq":id} }
                updatedVal = { "$set": { "config.status": "off" } }
                terminals.update_one(query,updatedVal)
            if st == "on":
                query = { "TID": {"$eq":id} }
                updatedVal = { "$set": { "config.status": "on" } }
                terminals.update_one(query,updatedVal)
            return redirect("/terminal/"+id)
    else:
        return redirect("/")
@app.route("/site/<id>",methods=["GET","POST"])
def siteDetail(id):
    if sessionCheck():
        s = getSiteById(id)
        return render_template("/siteDetail.html",title=TITLE,user=currentUser(),noti=None,site = s)
    else:
        return redirect("/")
@app.route("/sites",methods=["GET"])
def allSites():
    if sessionCheck():
        s = getSites()
        return render_template("sites.html",title=TITLE,user = currentUser(),noti=None,sites=s)
    else:
        return redirect("/")
@app.route("/terminals",methods=["GET"])
def allTerminals():
    if sessionCheck():
        t = getTerminals()
        return render_template("terminals.html",title=TITLE,user = currentUser(),noti = None,terminals = t,logs=getLogs())
    else:
        return redirect("/")

@app.errorhandler(Exception) 
def not_found(e):
  return render_template("500.html")
@app.errorhandler(404) 
def not_found1(e):
  return render_template("404.html")

@app.route("/all-vouchers",methods=["GET"])
def allVouchers():
    if sessionCheck():
        v = getVouchers()
        return render_template("allVouchers.html",title=TITLE,user = currentUser(),noti = None,vouchers = v)
    else:
        return redirect("/")
@app.route("/voucherT/<id>",methods=["GET"])
def voucherTransaction(id):
    if sessionCheck():
        t  = getVouchers({"TID":{"$eq":id}})[0]
        k = list(t.keys())
        k = k[1:]
        txt = {}
        for i in k:
            j = i.replace("_"," ")
            txt[i] = string.capwords(j)
        return render_template("voucherTransaction.html",title=TITLE,user = currentUser(),noti = None,transaction = t,keys = k,text = txt)
    else:
        return redirect("/")

@app.route("/updateUser",methods=["GET","POST"])
def update_user():
    if sessionCheck():
        if request.method == "GET":
            return redirect("/clients")
        if request.method  == "POST":
            global USERS
            username = request.form.get("username")
            password = request.form.get("password")
            type = request.form.get("type")
            USERS[username]['password'] = password
            USERS[username]['type'] = type   
            updateCred()
            LoadUsers()
            return redirect("/clients")
    else:
        return redirect("/")
@app.route("/deleteUser",methods=["GET","POST"])
def delete_user():
    if sessionCheck():
        if request.method == "GET":
            return redirect("/clients")
        if request.method  == "POST":
            global USERS
            username = request.form.get("username")
            USERS.pop(username)
            updateCred()
            LoadUsers()
            return redirect("/clients")
    else:
        return redirect("/")   
@app.route("/new-user",methods=["POST"])
def newUser():
    if sessionCheck():
        u = currentUser()
        global USERS
        if u['type'] == "root":
          
            s = {
                    "username":request.form.get("username"),
                    "password":request.form.get("password"),
                    "type":request.form.get("type"),
                    "last_login":"Hav'nt Logged Yet"
            }
            err = ""
            if s['username'] in USERS:
                err = err+"username already exists<br>"
            elif len(s['password']) <4:
                err =err+"password must be atleast 4 characters<br>"
            
            if err == "":
                USERS[s['username']] = s
                updateCred()
                LoadUsers()
                s = {}
            f = getUsers()

            return render_template("users.html",title=TITLE,user = currentUser(),noti=err,sess=s,users = f)
    else:
        return redirect("/")
@app.route("/clients",methods=["GET"])
def clientsDup():
    if sessionCheck():
        u = currentUser()
        if u['type'] == "root":
            f = getUsers()
            return render_template("users.html",title=TITLE,user = currentUser(),sess={},users = f)
        else:
            return redirect("/profile")
    return redirect("/clients-list")
@app.route("/client/<id>",methods=["GET"])
def clientDetail(id):
    if sessionCheck():
        c = getClients({"phone":{"$eq":id}})
        return render_template("client.html",title=TITLE,user = currentUser(),noti = None,clients = c)
    else:
        return redirect("/")
@app.route("/clients-list",methods=["GET"])
def clientsList():
    if sessionCheck():
        c = getClients()
        return render_template("clients.html",title=TITLE,user = currentUser(),noti = None, clients = c)
    else:
        return redirect("/")
@app.route("/voucher/<id>",methods = ["GET"])
def voucherDetail(id):
    if sessionCheck():
        t = getVouchers({"pin":{"$eq":id}})[0]
        #,rid,tid,dt,tm,ser,pin,plan
        g = VoucherGenerator(t["receipt_id"],t["TID"],t["date"],t["time"],t["service"],t["pin"],t["plan"])
        g.save_output()
        return render_template("voucherDetail.html",title=TITLE,user = currentUser(),noti = None,transaction = t)
    else:
        return redirect("/")

@app.route("/search-transactions",methods =["GET"])
def searchTransaction():
    return redirect("/all-transactions")

@app.route("/transaction/<id>",methods=["GET"])
def transactionDetail(id):
    if sessionCheck():
        t = getTransactions({"TID":{"$eq":id}})[0]
        k = list(t.keys())
        k = k[1:]
        txt = {}
        for i in k:
            j = i.replace("_"," ")
            txt[i] = string.capwords(j)
        return render_template("transactionDetail.html",title=TITLE,user = currentUser(),noti = None,transaction = t,keys = k,text = txt)
    else:
        return redirect("/")
@app.route("/reciept/<id>",methods=["GET"])
def recieptDetail(id):
    if sessionCheck():
        t = getTransactions({"receipt_id":{"$eq":id}})[0]
        g = ReceiptGenerator(t["receipt_id"],t["TID"],t["date"],t["time"],t["service"],t["phone"],t["total_payment"],t["pending_amount"])
        g.save_output()
        return render_template("recieptDetail.html",title=TITLE,user = currentUser(),noti = None,transaction = t)
    else:
        return redirect("/")
@app.route("/getBandwidth")
def getBd():
    tx = r.randint(1,10000)
    rx = r.randint(1,5000)
    return {"tx":tx,"rx":rx}
@app.route("/logout",methods = ["GET"])
def Logout():
    session.pop("user")
    return redirect("/")   

@app.route("/pending-transactions",methods=["GET"])
def pendingTransactions():
    if sessionCheck():
        args = request.args
        args = args.to_dict()
        trans = []
        fi_from = None
        fi_to = None
        if len(args)  >0:
            if "diff" in args.keys():                
                start_date = datetime.now() 
                to_Date = start_date + timedelta(days=-int(args.get("diff")))
                dts = date_range(to_Date,start_date)
                t = getTransactions({"pending_amount":{"$gt":"0"}})
                for i in dts:
                    for j in t:
                        k = i.strftime("%d/%m/%Y")
                        if j['date'] == k:
                            trans.append(j)
            elif "from" in args.keys() and "to" in args.keys():
                f = args.get("from")
                fi_from = f             
                f = f.split("-")
                f = f[2]+"/"+f[1]+"/"+f[0]
                t = args.get("to")
                fi_to = t
                t = t.split("-")
                t = t[2]+"/"+t[1]+"/"+t[0]
                fr = getDatefromString(f)
                to = getDatefromString(t)
                dts = date_range(fr,to)
                t = getTransactions({"pending_amount":{"$gt":"0"}})
                for i in dts:
                    for j in t:
                        k = i.strftime("%d/%m/%Y")
                        if j['date'] == k:
                            trans.append(j)
        else:
            trans = getTransactions({"pending_amount":{"$gt":"0"}})     
        fileLink = "P-"+getCurrentTimeStampClean()
        data =[]
        #headers = [['TID','Reciept #','Date','Time','Service','User','Amount','Pending']]
        for i in trans:
            a = [i["TID"],i["receipt_id"],i["date"],i["time"],i["service"],i["phone"],i["total_payment"],i["pending_amount"]]
            data.append(a)
        u = currentUser()
        fileLink = pdf(data,fileName=fileLink,user = u["username"])
        return render_template("pendingTransactions.html",title=TITLE,user = currentUser(),fr = fi_from,to=fi_to,noti = None,transactions = trans,pdfLink = fileLink)
    else:
        return redirect("/")  
@app.route("/all-transactions",methods=["GET"])
def allTransactions():
    if sessionCheck():
        args = request.args
        args = args.to_dict()
        trans = []
        fi_from = None
        fi_to = None
        if len(args)  >0:
            if "diff" in args.keys():                
                start_date = datetime.now() 
                to_Date = start_date + timedelta(days=-int(args.get("diff")))
                dts = date_range(to_Date,start_date)
                t = getTransactions()
                for i in dts:
                    for j in t:
                        k = i.strftime("%d/%m/%Y")
                        if j['date'] == k:
                            trans.append(j)
            elif "from" in args.keys() and "to" in args.keys():
                f = args.get("from")
                fi_from = f             
                f = f.split("-")
                f = f[2]+"/"+f[1]+"/"+f[0]
                t = args.get("to")
                fi_to = t
                t = t.split("-")
                t = t[2]+"/"+t[1]+"/"+t[0]
                fr = getDatefromString(f)
                to = getDatefromString(t)
                dts = date_range(fr,to)
                t = getTransactions()
                for i in dts:
                    for j in t:
                        k = i.strftime("%d/%m/%Y")
                        if j['date'] == k:
                            trans.append(j)
        else:
            trans = getTransactions() 

        
        fileLink = getCurrentTimeStampClean()
        data =[]
        #headers = [['TID','Reciept #','Date','Time','Service','User','Amount','Pending']]
        for i in trans:
            a = [i["TID"],i["receipt_id"],i["date"],i["time"],i["service"],i["phone"],i["total_payment"],i["pending_amount"]]
            data.append(a)
        u = currentUser()
        fileLink = pdf(data,fileName=fileLink,user = u["username"])
        return render_template("allTransactions.html",title=TITLE,user = currentUser(),fr = fi_from,to=fi_to,noti = None,transactions = trans,pdfLink = fileLink)
    else:
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
            c = len(getUsers())
            s = len(getTransactions())
            v = len(getVouchers())
            av = len(getTerminals()) 
            tt = len(getTerminals({"config.status":{"$eq":"on"}}))
            return render_template("index.html",user=currentUser(),total_terminals = numerize.numerize(av),title=TITLE,clients = numerize.numerize(c),sess=numerize.numerize(s),act_voucher=numerize.numerize(tt),vouchers=numerize.numerize(v))
        else:
            return render_template("login.html",title = TITLE)
    if request.method == "POST":
        user = request.form.get("user")
        pswd = request.form.get("password")
        if user in USERS:
            if USERS[user]["password"] == pswd:
                session["user"] = user
                USERS[user]["last_login"] = getCurrentTimeStamp()
                updateCred()
                LoadUsers()
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