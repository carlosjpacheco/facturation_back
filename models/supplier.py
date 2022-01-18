from sanic import request
from sanic_jwt_extended import JWT
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json
from utilities.validators import validSignup, validUpdateUser

async def addSupplier(request,data):
    try:
        valid = await validSignup(request)
        cursor = connectPSQL()
        if valid == True:
            postgres_insert_query = """ INSERT INTO supplier (rif,first_name,last_name,type_dni,fk_users) VALUES (%s,%s,%s,%s,%s)"""
            record_to_insert =(request["rif"],request["first_name"],request["last_name"],request["type_dni"],data)
            cursor["cursor"].execute(postgres_insert_query, record_to_insert)
            cursor["conn"].commit()
            return json({    
                "rif":request["rif"],
                "first_name":request["first_name"],
                "last_name":request["last_name"],
                "type_dni":request["type_dni"]})
    except (Exception, psycopg2.Error) as error:
        return json({"error":error},500)