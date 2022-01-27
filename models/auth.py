from sanic_jwt_extended import JWT
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json
from utilities.validators import validSignup, validUpdateUser


async def signup(request):
    try:
        valid = await validSignup(request)
        cursor = connectPSQL()
        if valid == True:
            postgres_insert_query = """ INSERT INTO users (username,psw,dni_rif,first_name,last_name,id_role,type_dni) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            record_to_insert =(request["username"],request["password"],request["dni_rif"],request["first_name"],request["last_name"],request["id_role"],request["type_dni"])
            cursor["cursor"].execute(postgres_insert_query, record_to_insert)
            cursor["conn"].commit()
            return json({"data":"Record inserted successfully into table"})
        else:
            return valid
    except (Exception, psycopg2.Error) as error:
        return json({"error":error},500)

def login(request):
    cursor = connectPSQL()

    
    sql_select_query = """SELECT * FROM users WHERE username = %s AND psw = %s"""

    cursor["cursor"].execute(sql_select_query, (request["username"],request["psw"],))

    user = cursor["cursor"].fetchone()
    if user:
        return json(
            {
                'data':{
                    'user': {
                            "id":user[0],
                            "username":user[1],
                            "password":user[2],
                            "dni_rif":user[3],
                            "name":user[4],
                            "last_name":user[5],
                            "id_role":user[6]},
                    'token': JWT.create_access_token(identity=user[0]),
                    'refresh': JWT.create_refresh_token(identity=user[0])                    
                },
                'type': 'auth',
                'code': 200
            }
        )
    else:
        return json({"error":"Usuario o contrasena incorrecta"})

async def updateUser(request,data):
    try:
        cursor = connectPSQL()
        valid = await validUpdateUser(request,data)
        if valid == True:
            if "username" in request:
                sql_update_query = """Update users set username = %s where id = %s"""
                cursor["cursor"].execute(sql_update_query, (request["username"],data,))
            if "id_role" in request:
                sql_update_query = """Update users set id_role = %s where id = %s"""
                cursor["cursor"].execute(sql_update_query, (request["id_role"],data,))
            if "psw" in request:
                sql_update_query = """Update users set psw = %s where id = %s"""
                cursor["cursor"].execute(sql_update_query, (request["psw"],data))
            if "first_name" in request:
                sql_update_query = """Update users set first_name = %s where id = %s"""
                cursor["cursor"].execute(sql_update_query, (request["first_name"],data))
            if "last_name" in request:
                sql_update_query = """Update users set last_name = %s where id = %s"""
                cursor["cursor"].execute(sql_update_query, (request["last_name"],data,))
            if "type_dni" in request:
                sql_update_query = """Update users set type_dni = %s where id = %s"""
                cursor["cursor"].execute(sql_update_query, (request["type_dni"],data,))
            cursor["conn"].commit()
            return json({"data":"Record Updated successfully"})
        return valid
    except (Exception, psycopg2.Error) as error:
        return json({"error":error},500)

async def deleteUser(request):
    try:
        cursor = connectPSQL()
        sql_delete_query = """Update users set status=false where id = %s"""
        cursor["cursor"].execute(sql_delete_query, (request["id"],))
        cursor["conn"].commit()
        return json({"data":"Usuario eliminado"})
    except (Exception, psycopg2.Error) as error:
        return json({"error":error},500)