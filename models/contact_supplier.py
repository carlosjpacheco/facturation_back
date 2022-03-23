from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json
from utilities.validators import validContactInfo

async def addContact(request):
    try:
        valid = await validContactInfo(request)
        cursor = connectPSQL()
        if valid == True:
            postgres_insert_query = """ INSERT INTO contact_supplier (first_name,last_name,phone_number,email) VALUES (%s,%s,%s,%s)"""
            record_to_insert =(request["first_name"],request["last_name"],request["phone_number"],request["email"],)
            cursor["cursor"].execute(postgres_insert_query, record_to_insert)
            cursor["conn"].commit()
            return json({"data":"Contacto agregado con éxito","supplier":{   
                "first_name":request["first_name"],
                "last_name":request["last_name"],
                "phone_number":request["phone_number"],
                "email":request["email"]
                },
                "code":200},200)
        return valid
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

def deleteContact(request,data):
    try:
        cursor = connectPSQL()
        sql_delete_query = """Delete from contact_supplier where id = %s"""
        cursor["cursor"].execute(sql_delete_query, (request["id"],data))
        cursor["conn"].commit()
        return json({"data":"Contacto eliminado con éxito","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def updateContact(request,data):
    try:
        cursor = connectPSQL()
        valid = await validContactInfo(request,data)
        if valid == True:
            if "first_name" in request:
                sql_update = """Update contact_supplier set first_name = %s where id = %s"""
                cursor["cursor"].execute(sql_update,(request["first_name"],request["id"],))
            if "last_name" in request:
                sql_update = """Update contact_supplier set last_name = %s where id = %s"""
                cursor["cursor"].execute(sql_update,(request["last_name"],request["id"],))
            if "email" in request:
                sql_update = """Update contact_supplier set email = %s where id = %s"""
                cursor["cursor"].execute(sql_update,(request["email"],request["id"],))
            if "phone_number" in request:
                sql_update = """Update contact_supplier set phone_number = %s where id = %s"""
                cursor["cursor"].execute(sql_update,(request["phone_number"],request["id"],))
            cursor["conn"].commit()
            return json({"data":"Contacto modificado con éxito","code":200},200)
        else:
            return valid
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

def readContact(request):
    try:
        cursor = connectPSQL()
        query_search = """SELECT * from contact_suppler WHERE id = %s"""
        cursor["cursor"].execute(query_search,(request["id"],))
        contact = cursor["cursor"].fetchone()
        if contact:
            return json({"data":{"contact":{"fisrt_name":contact[1],"last_name":contact[2],"phone_number":contact[3],"email":contact[4]}}})    
        else:
            return json({"data":"No se consiguio ningun usuario","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500) 