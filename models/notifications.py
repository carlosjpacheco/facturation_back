import time
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json

async def addNotification(request):
    try:
        print('HOLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaa')
        cursor = connectPSQL()
        query_noti = """INSERT INTO notifications (description,date,destination,read,source) VALUES (%s,%s,%s,%s,%s)"""
        records = (request["description"],str(time.time()),request["destination"],False,request['source'])
        cursor["cursor"].execute(query_noti,records)
        cursor["conn"].commit()
        return json({"data":"Notificación enviada","code":200},200)
    except (Exception, psycopg2.Error) as error:
        print(error)
        return json({"error":str(error),"code":500},500)

async def updateNotification(request,data):
    try:
        cursor = connectPSQL()
        query = """UPDATE notifications set read = True where destination = %s and id = %s"""
        cursor["cursor"].execute(query,(data,request["id"]))
        cursor["conn"].commit()
        return json({"data":"Marcada como leita","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def listNotifications(data):
    try:
        cont = 0
        notifications = []
        newNotifications=False
        cursor = connectPSQL()
        query_search = """SELECT * from notifications WHERE destination = %s"""
        cursor["cursor"].execute(query_search,(data,))
        noti = cursor["cursor"].fetchall()
        print(data)
        for x in noti:
            if x[3] == False:
                cont+=1
                newNotifications = True
            notifications.append({
                "id":x[0],
                'description':x[1],
                'date':x[5],
                'read':x[3]
            })
        return json({"data":notifications,"newNotification":newNotifications,"lenNewNoti":cont,"code":200},200)
    except(Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)