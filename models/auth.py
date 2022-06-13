from datetime import datetime
import base64
import hashlib
from os import curdir
import string
from sanic_jwt_extended import JWT
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json
from utilities.validators import validSignup, validUpdateUser
import random
from utilities.sendEmails import sendPswAdm

async def signup(request):
    try:
        valid = await validSignup(request)
        cursor = connectPSQL()
        request['psw'] = request['psw'].encode("utf-8")
        request['psw'] = base64.b64encode(request['psw']).decode()
        if valid == True:
            postgres_insert_query = """ INSERT INTO users (username,psw,dni_rif,first_name,last_name,id_role,type_dni,email) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
            record_to_insert =(request["username"],request["psw"],request["dni_rif"],request["first_name"],request["last_name"],request["id_role"],'V',request["email"])
            cursor["cursor"].execute(postgres_insert_query, record_to_insert)
            query_history = """INSERT INTO operation_history (description, id_user, date) VALUES (%s,%s,%s)"""
            records_history = ('Agregó un Nuevo Usuario',request["user_created"],datetime.now(),)
            cursor["cursor"].execute(query_history,records_history)
            cursor["conn"].commit()
            return json({"data":"Usuario creado con éxito","code":200},200)
        else:
            return valid
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

def login(request):
    try:
        cursor = connectPSQL()
        request['psw'] = request['psw'].encode("utf-8")
        request['psw'] = base64.b64encode(request['psw']).decode()
        # dec = base64.b64decode(request['psw']).decode()

        sql_select_query = """SELECT * FROM users WHERE username = %s AND psw = %s"""
        cursor["cursor"].execute(sql_select_query, (request["username"],str(request["psw"]),))
        user = cursor["cursor"].fetchone()

        if user:
            if user[8] == True:
                sql_update_query = """Update users set attemp = %s where username = %s"""
                cursor["cursor"].execute(sql_update_query, (0,request["username"]))
                cursor["conn"].commit()
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
            sql_select_query = """SELECT * FROM users WHERE username = %s"""
            cursor["cursor"].execute(sql_select_query, (request["username"],))
            user = cursor["cursor"].fetchone()
            if user:
                if user[10]+1==3:
                    sql_update_query = """Update users set attemp = %s,status = %s where username = %s"""
                    cursor["cursor"].execute(sql_update_query, ((user[10]+1),False,request["username"]))
                    cursor["conn"].commit()
                    return json({"error":"Su usuario se ha bloqueado, notificar al supervisor para activar el usuario","code":500},500)
                elif user[10]==10:
                    return json({"error":"Su usuario se ha bloqueado, notificar al supervisor para activar el usuario","code":500},500)
                else:
                    sql_update_query = """Update users set attemp = %s where username = %s"""
                    cursor["cursor"].execute(sql_update_query, ((user[10]+1),request["username"]))
            cursor["conn"].commit()


            return json({"error":"Usuario o contraseña incorrecta, al tercer intento se bloqueará","code":500},500)
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
            if "email" in request:
                sql_update_query = """Update users set email = %s where id = %s"""
                cursor["cursor"].execute(sql_update_query, (request["email"],request["id"],))
            if "dni_rif" in request:
                sql_update_query = """Update users set dni_rif = %s where id = %s"""
                cursor["cursor"].execute(sql_update_query, (request["dni_rif"],request["id"],))
            query_history = """INSERT INTO operation_history (description, id_user, date) VALUES (%s,%s,%s)"""
            records_history = ('Actualizo el Usuario '+request["username"],request["user_created"],datetime.now(),)
            cursor["cursor"].execute(query_history,records_history)
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
            sql_delete_query = """Update users set status=%s where id = %s"""
            cursor["cursor"].execute(sql_delete_query, (status,request["id"]))
        else:
            status = True
        sql_delete_query = """Update users set status=%s where id = %s"""
        cursor["cursor"].execute(sql_delete_query, (status,request["id"]))
        query_history = """INSERT INTO operation_history (description, id_user, date) VALUES (%s,%s,%s)"""
        records_history = ('Inactivó un Usuario',request["user_created"],datetime.now(),)
        cursor["cursor"].execute(query_history,records_history)
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
                "status": user[8],
                "email": user[9]}}})    
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

async def listUsersHistory(request):
    try:
        usersArrhistory = []
        cursor = connectPSQL()
        query_search = """SELECT * from operation_history where id_user = %s order by date desc"""
        cursor["cursor"].execute(query_search,(request['id'],))
        history = cursor["cursor"].fetchall()
        for x in history:
            historyJson = {
                "id":x[0],
                "description": x[1],
                "date": x[3].timestamp()
            }
            usersArrhistory.append(historyJson)
        return json({"data":usersArrhistory,"code":200},200)
    except (Exception,psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def listUsersOrder():
    try:
        usersArr = []
        cursor = connectPSQL()
        query_search = """SELECT * from users where id_role = 3 order by status desc"""
        cursor["cursor"].execute(query_search)
        users = cursor["cursor"].fetchall()
        for x in users:
            query_search = """SELECT COUNT(ord.id)
                                from purchase_order ord
                                WHERE ord.id_user = %s
                                and ord.id not in (SELECT id_purchase_order
                                FROM invoices); """
            cursor["cursor"].execute(query_search,(x[0],))
            orders = cursor["cursor"].fetchone()
            query_search = """SELECT COUNT(ord.id)
                                from purchase_order ord
                                WHERE ord.id_user = %s
                                and ord.id in (SELECT id_purchase_order
                                FROM invoices); """
            cursor["cursor"].execute(query_search,(x[0],))
            ordersP = cursor["cursor"].fetchone()
            usersJson = {
                "id":x[0],
                "name": x[4]+" "+x[5],
                "orders": orders[0],
                "ordersP":ordersP[0]
            }
            usersArr.append(usersJson)
            usersArr.sort(key=lambda p: p['orders'])
        return json({"data":usersArr,"code":200},200)
    except (Exception,psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def listUsersInvoice():
    try:
        usersArr = []
        cursor = connectPSQL()
        query_search = """SELECT * from users where id_role = 5 order by status desc"""
        cursor["cursor"].execute(query_search)
        users = cursor["cursor"].fetchall()
        for x in users:
            query_search = """SELECT COUNT(inv.id)
                                from invoices inv
                                WHERE inv.id_user = %s
                                and inv.id_status = 1; """
            cursor["cursor"].execute(query_search,(x[0],))
            orders = cursor["cursor"].fetchone()
            query_search = """SELECT COUNT(inv.id)
                                from invoices inv
                                WHERE inv.id_user = %s
                                and inv.id_status = 0; """
            cursor["cursor"].execute(query_search,(x[0],))
            ordersP = cursor["cursor"].fetchone()
            usersJson = {
                "id":x[0],
                "name": x[4]+" "+x[5],
                "orders": orders[0],
                "ordersP":ordersP[0]
            }
            usersArr.append(usersJson)
            usersArr.sort(key=lambda p: p['orders'])
        return json({"data":usersArr,"code":200},200)
    except (Exception,psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def UserRandomOrder():
    try:
        usersArr = []
        cursor = connectPSQL()
        query_search = """SELECT * from users where id_role = 3 order by status desc"""
        cursor["cursor"].execute(query_search)
        users = cursor["cursor"].fetchall()
        for x in users:
            query_search = """SELECT COUNT(ord.id)
                                from purchase_order ord
                                WHERE ord.id_user = %s
                                and ord.id not in (SELECT id_purchase_order
                                FROM invoices); """
            cursor["cursor"].execute(query_search,(x[0],))
            orders = cursor["cursor"].fetchone()
            usersJson = {
                "id":x[0],
                "name": x[4]+" "+x[5],
                "orders": orders[0]
            }
            usersArr.append(usersJson)
            usersArr.sort(key=lambda p: p['orders'])
            userid = usersArr[0]['id']
        return json({"data":userid,"code":200},200)
    except (Exception,psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def UserRandomInvoice():
    try:
        usersArr = []
        cursor = connectPSQL()
        query_search = """SELECT * from users where id_role = 5 order by status desc"""
        cursor["cursor"].execute(query_search)
        users = cursor["cursor"].fetchall()
        for x in users:
            query_search = """SELECT COUNT(inv.id)
                                from invoices inv
                                WHERE inv.id_user = %s
                                and inv.id_status = 1; """
            cursor["cursor"].execute(query_search,(x[0],))
            invoices = cursor["cursor"].fetchone()
            usersJson = {
                "id":x[0],
                "name": x[4]+" "+x[5],
                "invoices": invoices[0]
            }
            usersArr.append(usersJson)
            usersArr.sort(key=lambda p: p['invoices'])
            userid = usersArr[0]['id']
        return json({"data":userid,"code":200},200)
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
        query_search = """SELECT * from users WHERE id = %s"""
        cursor["cursor"].execute(query_search,(request["id"],))
        user = cursor["cursor"].fetchone()
        
        valid = await validUpdateUser(request)
        if valid == True:
            request['new_password'] = base64.b64encode(request['new_password'].encode("utf-8")).decode()
            print("PASO")
            sql_update_query = """Update users set psw = %s , username=%s where id = %s"""
            cursor["cursor"].execute(sql_update_query, (request["new_password"],request["username"],request["id"],))
            query_history = """INSERT INTO operation_history (description, id_user, date) VALUES (%s,%s,%s)"""
            records_history = ('Actualizó las Credenciales del Usuario '+request["username"],request["user_created"],datetime.now(),)
            cursor["cursor"].execute(query_history,records_history)
            cursor["conn"].commit()
            return json({"data":"Contrasena actualizada con éxito","code":200},200)
        else:
            return valid
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def forgotPassword(request):
    try:
        cursor = connectPSQL()
        sql_select_query = """SELECT * FROM users WHERE username = %s"""
        cursor["cursor"].execute(sql_select_query, (request["username"],))
        user = cursor["cursor"].fetchone()
        dec = base64.b64decode(user[2]).decode()
        sendPswAdm(user[9],'Su contraseña es:'+dec)
        return json({"data":"Se le ha enviado un correo con la recuperación de su contraseña","code":200},200)
    except Exception as error:
         return json({"data":str(error),"code":500},500)