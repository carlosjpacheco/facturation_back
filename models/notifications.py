from datetime import datetime
from queue import Empty
from sqlite3 import Cursor
from matplotlib import use
from numpy import empty
from sanic import request
from sanic_jwt_extended import JWT
from sqlalchemy import false
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json
from utilities.validators import validSignup, validSupplierInfo

def addNotification(request,data):
    try:
        cursor = connectPSQL()
        query_noti = """INSERT INTO notifications (description,date,destination,read,source) VALUES (%s,%s,%s,%s,%s)"""
        records = (request["description"],datetime.now(),request["destination"],false,data)
        cursor["cursor"].execute(query_noti,records)
        cursor["conn"].commit()
        return json({"data":"Notificación enviada"})
    except (Exception, psycopg2.Error) as error:
        return json({"error":error},500)

def updateNotification(data):
    try:
        cursor = connectPSQL()
        query = """UPDATE notifications set read = True where destination = %s"""
        cursor["cursor"].execute(query,data)
        cursor["conn"].commit()
        return empty()
    except (Exception, psycopg2.Error) as error:
        return json({"error":error},500)