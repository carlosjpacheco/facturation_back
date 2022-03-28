from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json
from utilities.validators import validSignup, validSupplierInfo,validUpdateSupplier

async def addSupplier(request):
    try:
        valid = await validSupplierInfo(request)
        cursor = connectPSQL()
        if valid == True:
            postgres_insert_query = """ INSERT INTO supplier (name, rif, fiscal_direction, phone, email,
                 contact_name, contact_lastname, contact_email, contact_phone)
                  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            record_to_insert =(request["name"],request["rif"],request["fiscal_direction"],request["phone"],
                                request["email"],request["contact_name"],request["contact_lastname"],request["contact_email"],
                                request["contact_phone"])
            cursor["cursor"].execute(postgres_insert_query, record_to_insert)
            cursor["conn"].commit()
            return json({"data":"Proveedor agregado con éxito","supplier":{   
                "rif":request["rif"],
                "name":request["name"]},
                "code":200},200)
        return valid
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

def deleteSupplier(request):
    try:
        cursor = connectPSQL()
        if request["status"] == True:
            status = False
        else:
            status = True
        sql_delete_query = """Update supplier set status=%s where id = %s"""
        cursor["cursor"].execute(sql_delete_query, (status,request["id"]))
        cursor["conn"].commit()
        return json({"data":"Proveedor eliminado con éxito","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def updateSupplier(request):
    try:
        cursor = connectPSQL()
        valid = await validUpdateSupplier(request)
        if valid == True:
            print(request)
            sql_update = """Update supplier set name=%s, rif=%s, fiscal_direction=%s, phone=%s, email=%s, contact_name=%s,
                                contact_lastname=%s, contact_email=%s, contact_phone=%s where id = %s"""
            cursor["cursor"].execute(sql_update,(request["name"],request["rif"],request["fiscal_direction"],
                                                request["phone"],request["email"],request["contact_name"],
                                                request["contact_lastname"],request["contact_email"],
                                                request["contact_phone"],request["id"],))
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
            supplierJson = {
                "id": x[0],
                "rif": x[2],
                "name": x[1],
                "email":x[5],
                "status":x[10],
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
            return json({"data":{"supplier":{"name":supplier[1],"rif":supplier[2],"fiscal_direction":supplier[3],
                                            "phone":supplier[4],"email":supplier[5],"contact_name":supplier[6],
                                            "contact_lastname":supplier[7],"contact_email":supplier[8],"contact_phone":supplier[9]}}})    
        else:
            return json({"data":"No se consiguio ningun usuario","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)