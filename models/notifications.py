import time
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json

def addNotification(request,data):
    try:
        cursor = connectPSQL()
        query_noti = """INSERT INTO notifications (description,date,destination,read,source) VALUES (%s,%s,%s,%s,%s)"""
        records = (request["description"],str(time.time()),request["destination"],False,data)
        cursor["cursor"].execute(query_noti,records)
        cursor["conn"].commit()
        return json({"data":"Notificación enviada"})
    except (Exception, psycopg2.Error) as error:
        return json({"error":error},500)

def updateNotification(request,data):
    try:
        cursor = connectPSQL()
        query = """UPDATE notifications set read = True where destination = %s and id = %s"""
        cursor["cursor"].execute(query,(data,request["id"]))
        cursor["conn"].commit()
        return json({"data":"ok"})
    except (Exception, psycopg2.Error) as error:
        return json({"error":error},500)