from sqlite3 import Cursor
from sanic import request
from sanic_jwt_extended import JWT
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json
from utilities.validators import validSignup, validSupplierInfo

async def addSupplier(request,data):
    try:
        valid = await validSignup(request)
        cursor = connectPSQL()
        if valid == True:
            postgres_insert_query = """ INSERT INTO supplier (rif,name,type_dni,fk_users) VALUES (%s,%s,%s,%s)"""
            record_to_insert =(request["rif"],request["name"],request["type_dni"],data)
            cursor["cursor"].execute(postgres_insert_query, record_to_insert)
            cursor["conn"].commit()
            return json({    
                "rif":request["rif"],
                "name":request["name"],
                "type_dni":request["type_dni"]})
    except (Exception, psycopg2.Error) as error:
        return json({"error":error},500)

def deleteSupplier(request,data):
    try:
        cursor = connectPSQL()
        sql_delete_query = """Delete from supplier where id = %s AND fk_user=%s"""
        cursor["cursor"].execute(sql_delete_query, (request["id"],data))
        cursor["conn"].commit()
        return json({"data":"Proveedor eliminado"})
    except (Exception, psycopg2.Error) as error:
        return json({"error":error},500)

async def updateSupplier(request,data):
    try:
        cursor = connectPSQL()
        valid = validSupplierInfo(request,data)
        if valid == True:
            if "name" in request:
                sql_update = """Update supplier set name = %s where id = %s"""
                cursor["cursor"].execute(sql_update,(request["name"],request["id"],))
            if "rif" in request:
                sql_update = """Update supplier set rif = %s where id = %s"""
                cursor["cursor"].execute(sql_update,(request["rif"],request["id"],))
            if "type_dni" in request:
                sql_update = """Update supplier set type_dni = %s where id = %s"""
                cursor["cursor"].execute(sql_update,(request["type_dni"],request["id"],))
            cursor["conn"].commit()
        else:
            return valid
    except (Exception, psycopg2.Error) as error:
        return json({"error":error},500)
    
def searchSupplier(request,data):
    try:
        cursor = connectPSQL()
    except (Exception, psycopg2.Error) as error:
        return json({"error":error},500)