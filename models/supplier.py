from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json
from utilities.validators import validSignup, validSupplierInfo

async def addSupplier(request,data):
    try:
        valid = await validSupplierInfo(request)
        cursor = connectPSQL()
        if valid == True:
            postgres_insert_query = """ INSERT INTO supplier (rif,name,type_dni,fk_users) VALUES (%s,%s,%s,%s)"""
            record_to_insert =(request["rif"],request["name"],request["type_dni"],data)
            cursor["cursor"].execute(postgres_insert_query, record_to_insert)
            cursor["conn"].commit()
            return json({"data":"Proveedor agregado con éxito","supplier":{   
                "rif":request["rif"],
                "name":request["name"],
                "type_dni":request["type_dni"]},
                "code":200},200)
        return valid
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

def deleteSupplier(request,data):
    try:
        cursor = connectPSQL()
        sql_delete_query = """Delete from supplier where id = %s AND fk_user=%s"""
        cursor["cursor"].execute(sql_delete_query, (request["id"],data))
        cursor["conn"].commit()
        return json({"data":"Proveedor eliminado con éxito","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def updateSupplier(request,data):
    try:
        cursor = connectPSQL()
        valid = await validSupplierInfo(request,data)
        if valid == True:
            if "name" in request:
                sql_update = """Update supplier set name = %s where id = %s"""
                cursor["cursor"].execute(sql_update,(request["name"],request["id"],))
            if "rif" in request:
                sql_update = """Update supplier set rif = %s where id = %s"""
                cursor["cursor"].execute(sql_update,(request["rif"],request["id"],))
            cursor["conn"].commit()
            return json({"data":"Usuario modificado con éxito","code":200},200)
        else:
            return valid
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)
    
def searchSupplier(request):
    try:
        cursor = connectPSQL()
        query_search = """SELECT * from supplier WHERE name = %s OR rif = %s"""
        cursor["cursor"].execute(query_search,(request["filter"],request["filter"],))
        user = cursor["cursor"].fetchone()
        if user:
            return json({"data":{"supplier":{"name":user[1],"rif":user[3]+"-"+user[2]}}})    
        else:
            return json({"data":"No se consiguio ningun usuario","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

def listSuppliers():
    try:
        
        supplierArr = []
        cursor = connectPSQL()
        query_search = """SELECT * from supplier"""
        cursor["cursor"].execute(query_search)
        supplier = cursor["cursor"].fetchall()
        for x in supplier:
            query_search = """SELECT * from contact_supplier WHERE id = %s"""
            cursor["cursor"].execute(query_search,(x[5],))
            contact = cursor["cursor"].fetchall()
            supplierJson = {
                "rif": x[2],
                "name": x[1],
                "type_dni": x[3],
                "email":x[5],
                "contact":{
                    "first_name":contact[0][1],
                    "last_name":contact[0][2],
                    "phone_number":contact[0][3],
                    "email":contact[0][4]
                }
            }
            supplierArr.append(supplierJson)
        return json({"data":supplierArr,"code":200},200)
    except (Exception,psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

def readSupplier(request):
    try:
        cursor = connectPSQL()
        query_search = """SELECT * from supplier WHERE id = %s"""
        cursor["cursor"].execute(query_search,(request["id"],))
        supplier = cursor["cursor"].fetchone()
        if supplier:
            return json({"data":{"supplier":{"name":supplier[1],"rif":supplier[3]+"-"+supplier[2]}}})    
        else:
            return json({"data":"No se consiguio ningun usuario","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)