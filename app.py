from __future__ import unicode_literals
from flask import Flask, session, redirect, request, render_template, jsonify, url_for
import mysql.connector
from mysql.connector import Error
import json
import os
import random
import requests
from dotenv import load_dotenv
load_dotenv()


host=os.getenv("host")
password=os.getenv("password")
partner_key=os.getenv("partner_key")


mydb = mysql.connector.connect(
    host=host,
    user="root",
    password=password,
    database="travelwebsite",
    charset="utf8"
)


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Pages


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

# /api/attractions 取得景點資料列表API
# 取得不同分頁的旅遊景點列表資料，也可以根據標題關鍵字篩選


@app.route("/api/attractions")
def get_attractions_api():

    page = request.args.get('page')
    pageind = int(request.args.get('page'))
    pagenum = pageind * 12

    keyword = (request.args.get('keyword'))

    failmessage = {
        "error": True,
        "message": "內部伺服器錯誤"
    }

    try:
        # print("Connection", mydb.is_connected())
        if mydb.is_connected() is True:

            # 先判斷篩選再判斷分頁
            # with no keyword，沒有給定則不做篩選
            if keyword == None or keyword == False or keyword == "":
                if pageind >= 0 and pageind < 27 and not None:
                    mycursor = mydb.cursor()
                    sql = "SELECT * FROM traveldt LIMIT  %s,12"
                    val = (pagenum,)
                    mycursor.execute(sql, val)
                    site = mycursor.fetchall()

                    data = []
                    for i in range(len(site)):
                        body = {
                            "id": site[i][0],
                            "name": site[i][1],
                            "category": site[i][2],
                            "description": site[i][3],
                            "address": site[i][4],
                            "transport": site[i][5],
                            "mrt": site[i][6],
                            "latitude": site[i][7],
                            "longitude": site[i][8],
                            "images": site[i][9].split(",")
                        },
                        data.append(body)
                    # 判斷是否是最後頁
                    print("Page", pageind)
                    if pageind == 26:
                        successmessage = {
                            "nextPage": None,
                            "data": data
                        }
                        return json.dumps(successmessage, ensure_ascii=False, indent=2), 200, {"Content-Type": "application/json"}
                    else:
                        successmessage = {
                            "nextPage": pageind+1,
                            "data": data
                        }
                        return json.dumps(successmessage, ensure_ascii=False, indent=2), 200, {"Content-Type": "application/json"}
            # with keyword，篩選景點名稱的關鍵字
            else:
                if pageind >= 0 and pageind < 27 and not None:
                    mycursor = mydb.cursor()
                    # 當頁
                    sql = 'SELECT * FROM traveldt WHERE name LIKE "%"%s"%" LIMIT %s,12'
                    val = (keyword, pagenum,)
                    mycursor.execute(sql, val)
                    site = mycursor.fetchall()
                    result_count = len(mycursor.fetchall())
                    # 全部
                    mycursor2 = mydb.cursor()
                    sql = 'SELECT * FROM traveldt WHERE name LIKE "%"%s"%"'
                    val = (keyword,)
                    mycursor2.execute(sql, val)
                    all_result_count = len(mycursor.fetchall())

                    data = []
                    for i in range(len(site)):
                        body = {
                            "id": site[i][0],
                            "name": site[i][1],
                            "category": site[i][2],
                            "description": site[i][3],
                            "address": site[i][4],
                            "transport": site[i][5],
                            "mrt": site[i][6],
                            "latitude": site[i][7],
                            "longitude": site[i][8],
                            "images": site[i][9].split(",")
                        }
                        data.append(body)  # 得到data

                    if all_result_count-(pagenum+12) > 0:
                        successmessage = {
                            "nextPage": pageind+1,
                            "data": data
                        }
                        return json.dumps(successmessage, ensure_ascii=False, indent=2), 200, {"Content-Type": "application/json"}
                    else:
                        successmessage_lessthan12 = {
                            "nextPage": None,
                            "data": data
                        }
                        return json.dumps(successmessage_lessthan12, ensure_ascii=False, indent=2), 200, {"Content-Type": "application/json"}
    except:
        # print("Except Section")
        return jsonify(failmessage), 500


# /api/attraction/{attractionId}API
# 根據景點編號取得景點資料

@app.route("/api/attraction/<int:attractionId>")
def get_attraction_api_byid(attractionId):
    path = int(request.path.replace("/api/attraction/", ""))
    try:
        if mydb.is_connected() is True:
            mycursor = mydb.cursor()
            sql = "SELECT * FROM traveldt WHERE id = %s"
            val = (attractionId,)
            mycursor.execute(sql, val)
            site = mycursor.fetchall()
            result_count = len(site)
            if path > 0 and path <= 319:
                successmessage = {
                    "data": {
                        "id": site[0][0],
                        "name": site[0][1],
                        "category": site[0][2],
                        "description": site[0][3],
                        "address": site[0][4],
                        "transport": site[0][5],
                        "mrt": site[0][6],
                        "latitude": site[0][7],
                        "longitude": site[0][8],
                        "images": site[0][9].split(",")
                    }
                }
                # print(mydb.is_connected())
                return json.dumps(successmessage, ensure_ascii=False, indent=2), 200, {"Content-Type": "application/json"}

            elif result_count == 0 or path == "" or path is False:
                failmessage = {
                    "error": True,
                    "message": "景點編號不正確"
                }

                return json.dumps(failmessage, ensure_ascii=False, indent=2), 400, {"Content-Type": "application/json"}

    except:
        failmessage2 = {
            "error": True,
            "message": "伺服器內部錯誤"
        }

        return json.dumps(failmessage2, ensure_ascii=False, indent=2), 500, {"Content-Type": "application/json"}


# 使用者相關api
@app.route("/api/user", methods=['GET'])
def user_get():


#     # 檢查使用者登入狀態
    if 'username' in session:
        email = session['username']
        mycursor = mydb.cursor()
    #         # 取出id
        sql = "SELECT id FROM user WHERE email=%s"
        val = (email, )
        mycursor.execute(sql, val)
        id = mycursor.fetchall()
        id = int(str(id)[2:len(id)-4])
    #         # 取出使用者姓名
        sql = "SELECT username FROM user WHERE email=%s"
        val = (email,)
        mycursor.execute(sql, val)
        name = mycursor.fetchall()
        name = str(name)[3:len(name)-5]

        successmessage = {
                        "data": {
                            "id": id,
                            "name": name,
                            "email": email
                        }
                        }

        return json.dumps(successmessage, ensure_ascii=False, indent=2), 200, {"Content-Type": "application/json"}
    else:
        # null 表示未登入
        failmessage = {"data": None}

        return json.dumps(failmessage, ensure_ascii=False), 500, {"Content-Type": "application/json"}

# 註冊


@app.route("/api/user", methods=['POST'])
def user_post():
    try:
        if mydb.is_connected() is True:

            data = request.get_data()
            data = json.loads(data)
            email = data['email']
            name = data['name']
            password = data['password']

            mycursor = mydb.cursor()
            sql = "SELECT username FROM user where email=%s"
            val = (email,)
            mycursor.execute(sql, val)
            result_count = len(mycursor.fetchall())

            if result_count >= 1:
                failmessage = {
                                "error": True,
                                "message": "重複的 Email"
                                }
                return json.dumps(failmessage, ensure_ascii=False, indent=2), 400, {"Content-Type": "application/json"}
            else:

                sql = "INSERT INTO user (username,email,password) VALUES (%s, %s, %s)"
                val = (name, email, password)
                mycursor.execute(sql, val)
                mydb.commit()
                successmessage = {
                                    "ok": True,
                                    }

                return json.dumps(successmessage, ensure_ascii=False, indent=2), 200, {"Content-Type": "application/json"}
    except:
        failmessage2 = {
            "error": True,
            "message": "伺服器內部錯誤"
        }

        return json.dumps(failmessage2, ensure_ascii=False, indent=2), 500, {"Content-Type": "application/json"}
# 登入


@app.route("/api/user", methods=['PATCH'])
def user_patch():
    try:
        if mydb.is_connected() is True:
            data = request.get_data()
            data = json.loads(data)
            email = data['email']
            password = data['password']
            sql = "SELECT id FROM user WHERE email=%s and password=%s"
            val = (email, password)
            mycursor = mydb.cursor()
            mycursor.execute(sql, val)
            result = mycursor.fetchall()

#             # 判斷是否有找到符合條件的帳密
            if result == []:
#                 # 驗證失敗
                failmessage = {
                    "error": True,
                    "message": "帳號或密碼錯誤"
                }

                return json.dumps(failmessage, ensure_ascii=False, indent=2), 400, {"Content-Type": "application/json"}
            else:
#                 
#                 # 將mail加入 session 中紀錄
                session['username'] = email

                successmessage = {
                                "ok": True
                                }
                return json.dumps(successmessage, ensure_ascii=False, indent=2), 200, {"Content-Type": "application/json"}

    except:
        failmessage = {
            "error": True,
            "message": "伺服器內部錯誤"
        }

        return json.dumps(failmessage, ensure_ascii=False, indent=2), 500, {"Content-Type": "application/json"}


# 登出
@app.route("/api/user", methods=['DELETE'])
def signout():
    # 連線到【登出功能網址】，在後端Session 中記錄使用者狀態為未登入
    session.pop('username', None)
    successmessage = {
                    "ok": True
                    }
    return json.dumps(successmessage, ensure_ascii=False, indent=2), 200, {"Content-Type": "application/json"}

# 取得未送出的預定行程
@app.route("/api/booking", methods=['GET'])
def reservation_get(): 
    try:
        if mydb.is_connected() is True:
            if 'username' in session:
                email=session['username']                
            
                mycursor = mydb.cursor()                               
                sql = "SELECT attractionId FROM bookings WHERE mail=%s ORDER BY id DESC LIMIT 0,1"
                val = (email,)
                mycursor.execute(sql, val)
                id = mycursor.fetchall()
                id = int(str(id)[2:len(id)-4])
                
                sql = "SELECT * FROM traveldt WHERE id = %s"
                val = (id,)
                mycursor.execute(sql, val)
                site = mycursor.fetchall()                   
                
                sql = "SELECT date FROM bookings WHERE mail=%s ORDER BY id DESC LIMIT 0,1"
                val = (email,)
                mycursor.execute(sql, val)
                date = mycursor.fetchall()
                date = str(date)[16:len(date)-5].replace(',',' -')
                
                sql = "SELECT time FROM bookings WHERE mail=%s ORDER BY id DESC LIMIT 0,1"
                val = (email,)
                mycursor.execute(sql, val)
                time = mycursor.fetchall()
                time = str(time)[3:len(time)-5]
                
                sql = "SELECT price FROM bookings WHERE mail=%s ORDER BY id DESC LIMIT 0,1"
                val = (email,)
                mycursor.execute(sql, val)
                price = mycursor.fetchall()
                price = int(str(price)[2:len(price)-4])                    

                successmessage={
                    "data": {
                        "attraction": {
                            "id": site[0][0],
                            "name": site[0][1],
                            "address": site[0][4],
                            "image": site[0][9].split(",")[0]
                        },
                        "date":date,
                        "time":time,
                        "price":price,
                    }
                }

                return json.dumps(successmessage, ensure_ascii=False, indent=2), 200, {"Content-Type": "application/json"} 
                            
            else:
                failmessage = {
                    "error": True,
                    "message": "未登入系統，拒絕存取"
                }

                return json.dumps(failmessage, ensure_ascii=False, indent=2), 403, {"Content-Type": "application/json"}
    except:
        failmessage2 = {
            "error": True,
            "message": "伺服器內部錯誤"
        }

        return json.dumps(failmessage2, ensure_ascii=False, indent=2), 500, {"Content-Type": "application/json"}


    

# 建立新的預定行程

@app.route("/api/booking", methods=['POST'])
def reservation():

    try:
        if mydb.is_connected() is True:
            data = request.get_data()
            data = json.loads(data)
            attractionId= data['attractionId']
            date= data['date']
            time=data['time']
            price= data['price']
            
            if 'username' in session:
                mail = session['username']
                mycursor = mydb.cursor()
                sql = "INSERT INTO bookings (attractionId, date, time, price, mail) VALUES (%s, %s, %s, %s, %s)"
                val = (attractionId, date, time, price, mail,)
                mycursor.execute(sql, val)
                mydb.commit()
                successmessage = {
                                    "ok": True,
                                    }

                return json.dumps(successmessage, ensure_ascii=False, indent=2), 200, {"Content-Type": "application/json"}
            elif date or time or price == None or False or "" :
                fail = {
                                "error": True,
                                "message": "建立失敗，輸入不正確或其他原因"
                                }

                return json.dumps(fail, ensure_ascii=False, indent=2), 400, {"Content-Type": "application/json"}
            elif 'username' not in session: 
                failmessage = {
                    "error": True,
                    "message": "未登入系統，拒絕存取"
                }

                return json.dumps(failmessage, ensure_ascii=False, indent=2), 403, {"Content-Type": "application/json"}
    except:
        failmessage = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return json.dumps(failmessage, ensure_ascii=False, indent=2), 500, {"Content-Type": "application/json"}

@app.route("/api/booking", methods=['DELETE'])
def cancel():
    if 'username' in session:
        mail = session['username']
        mycursor = mydb.cursor()
        sql = "DELETE FROM bookings WHERE mail=%s"
        val = (mail,)
        mycursor.execute(sql, val)
        mydb.commit()
        successmessage = {
                        "ok": True
                        }
        return json.dumps(successmessage, ensure_ascii=False, indent=2), 200, {"Content-Type": "application/json"}
    else:
        failmessage = {
            "error": True,
            "message": "未登入系統，拒絕存取"
        }

        return json.dumps(failmessage, ensure_ascii=False, indent=2), 403, {"Content-Type": "application/json"}

@app.route("/api/orders", methods=['POST'])
def orders():

    try:
        if mydb.is_connected() is True:
            data = request.get_data()
            data = json.loads(data)
            prime= data['prime']
            price= data['order']['price']
            
            if 'username' in session:
                session['prime']=prime
                session['paid']='N'
                session['bookingID']=random.randrange(5, 50)
                
                req_url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"

                #pay by prime 資料
                formdata = {
                            "prime": str(session['prime']),
                            "partner_key": partner_key,
                            "merchant_id": "jhihhan_ESUN",
                            "details":"TapPay Test",
                            "amount": price,
                            "cardholder": {
                                "phone_number": "+886923456789",
                                "name": "王小明",
                                "email": "LittleMing@Wang.com",
                                "zip_code": "100",
                                "address": "台北市天龍區芝麻街1號1樓",
                                "national_id": "A123456789"
                            },
                            "remember": True
                }
                
                json_str = json.dumps(formdata)

                #request header
                req_header = {
                    'Content-Type': 'application/json',
                    'x-api-key': partner_key
                }
                #發出請求
                response = requests.post(
                    req_url, 
                    data = json_str, 
                    headers = req_header
                )

                print (response.text)
                if json.loads(response.text)['msg']=='Success':
                    session['paid']='Y'
                    print(session['paid'])
                    message ={
                                "data": {
                                    "number": "20210425121135",
                                    "payment": {
                                    "status": 0,
                                    "message": "付款成功"
                                    }
                                },
                                "bookingID":session['bookingID']
                            }
                    
                    mail = session['username']
                    mycursor = mydb.cursor()
                    sql = "DELETE FROM bookings WHERE mail=%s"
                    val = (mail,)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    
                    return json.dumps(message, ensure_ascii=False, indent=2), 200, {"Content-Type": "application/json"}  
                else:
                    session['paid']='N'
                    message ={
                                "data": {
                                    "number": "",
                                    "payment": {
                                    "status": 0,
                                    "message": "付款失敗"
                                    }
                                },
                                "bookingID":session['bookingID']
                            }
                    return json.dumps(message, ensure_ascii=False, indent=2), 200, {"Content-Type": "application/json"}

            elif session['bookingID']=="":
                failmessage = {
                    "error": True,
                    "message": "訂單建立失敗，輸入不正確或其他原因"
                }

                return json.dumps(failmessage, ensure_ascii=False, indent=2), 400, {"Content-Type": "application/json"}
            elif 'username' not in session: 
                failmessage = {
                    "error": True,
                    "message": "未登入系統，拒絕存取"
                }

                return json.dumps(failmessage, ensure_ascii=False, indent=2), 403, {"Content-Type": "application/json"}
    except:
        failmessage = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return json.dumps(failmessage, ensure_ascii=False, indent=2), 500, {"Content-Type": "application/json"}



app.run(host="0.0.0.0",port=3000)