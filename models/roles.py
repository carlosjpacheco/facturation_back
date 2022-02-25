from utilities.connections import connectPSQL
from sanic.response import json
from utilities.validators import validRol

async def addRole(request):
    try:
        cursor = connectPSQL()
        isValid = await validRol(request)
        if isValid == True:
            postgres_insert_query = """ INSERT INTO role (name) VALUES (%s)"""
            cursor["cursor"].execute(postgres_insert_query, (request["name"],))
            cursor["conn"].commit()
            return json({"data":"Nuevo rol agregado con éxito","code":200},200)
        else:
            return isValid
    except Exception as error:
        return json({"error":str(error),"code":500},500)

async def addPermissionsToRol(request):
    try:
        cursor = connectPSQL()
        query_search = """SELECT * from role WHERE name = %s"""
        cursor["cursor"].execute(query_search,(request["name"],))
        role = cursor["cursor"].fetchone()
        if role:
            for x in request["permissions"]:
                    postgres_insert_query = """ INSERT INTO rol_perm (id_role,id_permissions) VALUES (%s,%s)"""
                    record_to_insert =(role[0],x)
                    cursor["cursor"].execute(postgres_insert_query, record_to_insert)
                    cursor["conn"].commit()
            return json({"data":"Permisos agregados con éxito","code":200},200)
    except Exception as error:
        return json({"error":str(error),"code":500},500)