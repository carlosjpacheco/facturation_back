import time
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json


def addRole(request):
    try:
        cursor = connectPSQL()
        postgres_insert_query = """ INSERT INTO role (name) VALUES (%s)"""
        record_to_insert =(request["name"])
        cursor["cursor"].execute(postgres_insert_query, record_to_insert)
        cursor["conn"].commit()
    except Exception as error:
        return json({"error":str(error),"code":500},500)

def addPermissionsToRol(request):
    try:
        cursor = connectPSQL()
        query_search = """SELECT * from role WHERE name = %s"""
        cursor["cursor"].execute(query_search,(request["name"],))
        role = cursor["cursor"].fetchone()
        for x in request["permissions"]:
                postgres_insert_query = """ INSERT INTO rol_perm (id_rol,id_perm) VALUES (%s,%s)"""
                record_to_insert =(role[0],x)
                cursor["cursor"].execute(postgres_insert_query, record_to_insert)
                cursor["conn"].commit()
    except Exception as error:
        return json({"error":str(error),"code":500},500)