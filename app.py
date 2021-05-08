from __future__ import unicode_literals
from flask import Flask, session, redirect, request, render_template, jsonify, url_for
import mysql.connector
from mysql.connector import Error
import json
import os
import requests








mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="ella223567",
    database="travelwebsite",
    charset= "utf8"
)



app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

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

    page=request.args.get('page')
    pageind=int(request.args.get('page'))
    pagenum = pageind *12
    
    keyword=(request.args.get('keyword'))
    
    failmessage = {
        "error": True,
        "message": "內部伺服器錯誤"
    }
    
    try:
        # print("Connection", mydb.is_connected())
        if mydb.is_connected() is True:   
    
            #先判斷篩選再判斷分頁    
            #with no keyword，沒有給定則不做篩選
            if keyword == None or keyword ==False or keyword =="":
                if pageind >= 0 and pageind <27 and  not None:
                    mycursor = mydb.cursor()
                    sql = "SELECT * FROM traveldt LIMIT  %s,12"
                    val = (pagenum,)
                    mycursor.execute(sql, val)
                    site = mycursor.fetchall()

                    data= []
                    for i in range(len(site)):
                        body={
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
                    #判斷是否是最後頁
                    print("Page", pageind)
                    if pageind==26:
                        successmessage = {
                            "nextPage": None,
                            "data": data
                        }
                        return json.dumps(successmessage,ensure_ascii=False,indent=2), 200 , {"Content-Type": "application/json"}
                    else:        
                        successmessage = {
                            "nextPage": pageind+1,
                            "data": data
                        }
                        return json.dumps(successmessage,ensure_ascii=False,indent=2), 200 , {"Content-Type": "application/json"}
            #with keyword，篩選景點名稱的關鍵字
            else:
                if pageind >= 0 and pageind <27 and  not None:
                    mycursor = mydb.cursor()
                    #當頁
                    sql = 'SELECT * FROM traveldt WHERE name LIKE "%"%s"%" LIMIT %s,12'
                    val = (keyword,pagenum,)
                    mycursor.execute(sql, val)
                    site = mycursor.fetchall()
                    result_count = len(mycursor.fetchall())
                    #全部
                    mycursor2 = mydb.cursor()           
                    sql = 'SELECT * FROM traveldt WHERE name LIKE "%"%s"%"'
                    val = (keyword,)
                    mycursor2.execute(sql, val)
                    all_result_count = len(mycursor.fetchall())
                    
                    data= []
                    for i in range(len(site)):
                        body={
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
                        data.append(body)#得到data
                    
                    if all_result_count-(pagenum+12)>0:        
                        successmessage = {
                        "nextPage": pageind+1,
                        "data": data
                        }
                        return json.dumps(successmessage,ensure_ascii=False,indent=2), 200 , {"Content-Type": "application/json"}
                    else:
                        successmessage_lessthan12 = {
                        "nextPage": None,
                        "data": data
                        }
                        return json.dumps(successmessage_lessthan12,ensure_ascii=False,indent=2), 200 , {"Content-Type": "application/json"}
    except :
        # print("Except Section")
        return jsonify(failmessage),500
        
        
# /api/attraction/{attractionId}API
# 根據景點編號取得景點資料

@app.route("/api/attraction/<int:attractionId>")
def get_attraction_api_byid(attractionId):
    path=int(request.path.replace("/api/attraction/", ""))
    try:
        if mydb.is_connected() is True:
            mycursor = mydb.cursor()
            sql = "SELECT * FROM traveldt WHERE id = %s"
            val=(attractionId,)
            mycursor.execute(sql, val)
            site=mycursor.fetchall()
            result_count = len(site)
            if path > 0 and path <=319:
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
                print(mydb.is_connected())
                return json.dumps(successmessage,ensure_ascii=False,indent=2), 200 , {"Content-Type": "application/json"}
                
            elif  result_count==0 or path=="" or path is False:
                failmessage = {
                    "error": True,
                    "message": "景點編號不正確"
                }

                return json.dumps(failmessage,ensure_ascii=False,indent=2), 400 , {"Content-Type": "application/json"}
            
    except :
        failmessage2 = {
            "error": True,
            "message": "伺服器內部錯誤"
        }

        return json.dumps(failmessage2,ensure_ascii=False,indent=2), 500 , {"Content-Type": "application/json"}
        
app.run(port=3000)