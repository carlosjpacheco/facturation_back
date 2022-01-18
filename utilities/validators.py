import re
from utilities.connections import connectPSQL
from sanic.response import json

async def validSignup(request):
    cursor = connectPSQL()
    if "username" in request:
        username_query= """SELECT * FROM users WHERE username= %s"""
        cursor['cursor'].execute(username_query,(request['username'],))
        if cursor["cursor"].fetchone():
            return json({"error":"Username no disponible"})
    if "dni_rif" in request:
        dni_rif_query= """SELECT * FROM users WHERE dni_rif= %s"""
        cursor['cursor'].execute(dni_rif_query,(request['dni_rif'],))
        if cursor["cursor"].fetchone():
            return json({"error":"Ya existe un usuario con el mismo numero de dni_rif"})
    if "rif" in request:
        dni_rif_query= """SELECT * FROM supplier WHERE rif= %s"""
        cursor['cursor'].execute(dni_rif_query,(request['rif'],))
        if cursor["cursor"].fetchone():
            return json({"error":"Ya existe un proveedor con el mismo numero de rif"})
    return True

async def validUpdateUser(request,data):

    cursor = connectPSQL()
    user_query = """SELECT * FROM users WHERE id = %s"""
    cursor["cursor"].execute(user_query,(data,))
    user = cursor["cursor"].fetchone()
    if user:
        if "username" in request:
            if request["username"]==user[1]:
                return json({"error":"El nuevo username no puede ser el que ya esta en uso"})
            search_user_query = """SELECT * FROM users WHERE username= %s"""
            cursor["cursor"].execute(search_user_query,(request["username"],))
            search_user = cursor["cursor"].fetchone()
            if search_user:
                return json({"error":"Username no disponible"})
    return True

async def validSupplierInfo(request,data):
    cursor = connectPSQL()
    if "name" in request:
        sql_query = """SELECT * from supplier WHERE name = %s AND fk_users = %s"""
        cursor["cursor"].execute(sql_query,(request["name"],data,))
        user = cursor["cursor"].fetchone()
        if user:
            return json({"error":"Ya tiene un proveedor registrado con ese nombre"})
    if "rif" in request:
        sql_query = """SELECT * from supplier WHERE rif = %s AND fk_users = %s"""
        cursor["cursor"].execute(sql_query,(request["rif"],data,))
        user = cursor["cursor"].fetchone()
        if user:
            return json({"error":"Ya tiene un proveedor registrado con ese rif"})
    return True