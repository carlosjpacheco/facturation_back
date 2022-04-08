import hashlib
from os import curdir
from sanic_jwt_extended import JWT
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json
from utilities.validators import validSignup, validUpdateUser

async def signup(request):
    try:
        valid = await validSignup(request)
        cursor = connectPSQL()
        request["psw"]= hashlib.sha256(str(request["psw"]).encode()).hexdigest()
        if valid == True:
            postgres_insert_query = """ INSERT INTO users (username,psw,dni_rif,first_name,last_name,id_role,type_dni) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            record_to_insert =(request["username"],request["psw"],request["dni_rif"],request["first_name"],request["last_name"],request["id_role"],'V')
            cursor["cursor"].execute(postgres_insert_query, record_to_insert)
            cursor["conn"].commit()
            return json({"data":"Usuario creado con éxito","code":200},200)
        else:
            return valid
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

def login(request):
    try:
        cursor = connectPSQL()
        request["psw"] = hashlib.sha256(str(request["psw"]).encode()).hexdigest()
        # print(str(request["psw"]))
        sql_select_query = """SELECT * FROM users WHERE username = %s AND psw = %s"""

        cursor["cursor"].execute(sql_select_query, (request["username"],str(request["psw"]),))

        user = cursor["cursor"].fetchone()
        if user:
            if user[8] == True:
                return json(
                    {
                        'data':{
                            'user': {
                                    "id":user[0],
                                    "username":user[1],
                                    "dni_rif":user[3],
                                    "name":user[4],
                                    "last_name":user[5],
                                    "rol":user[6]
                                    },
                            'token': JWT.create_access_token(identity=user[0]),
                            'refresh': JWT.create_refresh_token(identity=user[0])                    
                        },
                        'code': 200
                    }
                )
            else:
                return json({"error":"Usuario Inactivo","code":500},500)
        else:
            return json({"error":"Usuario o contraseña incorrecta","code":500},500)
    except Exception as error:
        return json({"error":str(error),"code":500},500)

async def updateUser(request):
    try:
        cursor = connectPSQL()
        valid = await validUpdateUser(request)
        if valid == True:
            if "username" in request:
                sql_update_query = """Update users set username = %s where id = %s"""
                cursor["cursor"].execute(sql_update_query, (request["username"],request["id"],))
            if "id_role" in request:
                sql_update_query = """Update users set id_role = %s where id = %s"""
                cursor["cursor"].execute(sql_update_query, (request["id_role"],request["id"],))
            if "psw" in request:
                sql_update_query = """Update users set psw = %s where id = %s"""
                cursor["cursor"].execute(sql_update_query, (request["psw"],request["id"]))
            if "first_name" in request:
                sql_update_query = """Update users set first_name = %s where id = %s"""
                cursor["cursor"].execute(sql_update_query, (request["first_name"],request["id"]))
            if "last_name" in request:
                sql_update_query = """Update users set last_name = %s where id = %s"""
                cursor["cursor"].execute(sql_update_query, (request["last_name"],request["id"],))
            if "dni_rif" in request:
                sql_update_query = """Update users set dni_rif = %s where id = %s"""
                cursor["cursor"].execute(sql_update_query, (request["dni_rif"],request["id"],))
            cursor["conn"].commit()
            return json({"data":"Usuario actualizado con éxito","code":200},200)
        return valid
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def deleteUser(request):
    try:
        cursor = connectPSQL()
        if request["status"] == True:
            status = False
        else:
            status = True
        sql_delete_query = """Update users set status=%s where id = %s"""
        cursor["cursor"].execute(sql_delete_query, (status,request["id"]))
        cursor["conn"].commit()
        return json({"data":"Usuario eliminado","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def readUser(request):
    try:
        cursor = connectPSQL()
        query_search = """SELECT * from users WHERE id = %s"""
        cursor["cursor"].execute(query_search,(request["id"],))
        user = cursor["cursor"].fetchone()
        if user:
            query_search = """SELECT * from role WHERE id = %s"""
            cursor["cursor"].execute(query_search,(str(user[6])))
            rol = cursor["cursor"].fetchone()
            return json({"data":{"user":{
                "id":user[0],
                "username": user[1],
                "dni_rif": user[3],
                "first_name": user[4],
                "last_name": user[5],
                "role":rol[0],
                "type_dni": user[7],
                "status": user[8]}}})    
        else:
            return json({"data":"No se consiguio ningun usuario","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":error,"code":500},500)

async def listUsers():
    try:
        usersArr = []
        cursor = connectPSQL()
        query_search = """SELECT * from users order by status desc"""
        cursor["cursor"].execute(query_search)
        users = cursor["cursor"].fetchall()
        for x in users:
            query_search = """SELECT * from role WHERE id = %s"""
            cursor["cursor"].execute(query_search,(str(x[6])))
            rol = cursor["cursor"].fetchone()
            usersJson = {
                "id":x[0],
                "username": x[1],
                "dni_rif": x[3],
                "first_name": x[4],
                "last_name": x[5],
                "role":rol[1],
                "status": x[8]
            }
            usersArr.append(usersJson)
        return json({"data":usersArr,"code":200},200)
    except (Exception,psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)


async def searchUser(request):
    try:
        cursor = connectPSQL()
        query_search = """SELECT * from users WHERE username = %s OR dni_rif = %s OR first_name = %s OR last_name = %s """
        cursor["cursor"].execute(query_search,(request["filter"],request["filter"],request["filter"],request["filter"],))
        user = cursor["cursor"].fetchone()
        if user:
            if user:
                query_search = """SELECT * from role WHERE id = %s"""
                cursor["cursor"].execute(query_search,(str(user[6])))
                rol = cursor["cursor"].fetchone()
                return json({"data":{"user":{"username": user[1],
                    "dni_rif": user[3],
                    "first_name": user[4],
                    "last_name": user[5],
                    "role":rol[1],
                    "status": user[8]}}}) 
        else:
            return json({"data":"No se consiguio ningun usuario","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)


async def updatePassword(request):
    try:
        cursor = connectPSQL()
        request["password"]= hashlib.sha256(str(request["password"]).encode()).hexdigest()
        query_search = """SELECT * from users WHERE id = %s AND psw= %s"""
        cursor["cursor"].execute(query_search,(request["id"],request["password"]))
        user = cursor["cursor"].fetchone()
        
        if user:
            valid = await validUpdateUser(request)
            if valid == True:
                request["new_password"]= hashlib.sha256(str(request["new_password"]).encode()).hexdigest()
                sql_update_query = """Update users set psw = %s , username=%s where id = %s"""
                cursor["cursor"].execute(sql_update_query, (request["new_password"],request["username"],request["id"],))
                cursor["conn"].commit()
                return json({"data":"Contrasena actualizada con éxito","code":200},200)
            else:
                return valid
        else:
            return json({"error":"Contrasena incorrecta, por favor verifique y vuelva a intentar","code":500},500)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)