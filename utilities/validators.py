from utilities.connections import connectPSQL
from sanic.response import json

async def validSignup(request):
    cursor = connectPSQL()
    username_query= """SELECT * FROM users WHERE username= %s"""
    cursor['cursor'].execute(username_query,(request['username'],))
    if cursor["cursor"].fetchone():
        return json({"error":"Username no disponible"})
    dni_rif_query= """SELECT * FROM users WHERE dni_rif= %s"""
    cursor['cursor'].execute(dni_rif_query,(request['dni_rif'],))
    if cursor["cursor"].fetchone():
        return json({"error":"Ya existe un usuario con el mismo numero de dni_rif"})
    return True

async def validUpdateUser(request,data):
    cursor = connectPSQL()
    user_query = """SELECT * FROM users WHERE dni_rif= %s"""
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
