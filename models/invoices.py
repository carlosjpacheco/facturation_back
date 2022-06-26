from datetime import datetime
import os
from models.notifications import addNotification
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json

from utilities.validators import validInvoice

async def addInvoice(request,data):
    try:
        valid = await validInvoice(request)
        if valid == True:
            query_search = """SELECT * from invoices WHERE nro_invoice = %s and name_supplier = %s"""
            cursor["cursor"].execute(query_search,(request["nro_invoice"],request["supplier"],))
            invoice = cursor["cursor"].fetchone()
            if invoice:
                return json({"error":"La Factura ya fue procesada","code":500},500)        
            else:
                cursor = connectPSQL()
                query_noti = """INSERT INTO invoices (nro_invoice,id_user,total,id_status,id_purchase_order,paid,created_at,deleted,date,name_supplier,paid_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                records = (request["nro_invoice"],None,float(request["total"]),1,request["id_purchase_order"],False,None,False,request["date"],request["supplier"],None,)
                cursor["cursor"].execute(query_noti,records)
                cursor["conn"].commit()
                addInvoiceDetail(request)
                return json({"data":"Factura creada","code":200},200)
        else:
            return valid
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def delInvoice(request):
    try:
        cursor = connectPSQL()
        sql_delete_query = """Update invoices set deleted=true where id = %s"""
        cursor["cursor"].execute(sql_delete_query, (request["id"],))
        cursor["conn"].commit()
        return json({"data":"Factura eliminada","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def readInvoice(request):
    try:
        cursor = connectPSQL()
        query_search = """SELECT * from invoices WHERE id = %s"""
        cursor["cursor"].execute(query_search,(request["id"],))
        invoice = cursor["cursor"].fetchone()
        query_search = """SELECT * from status WHERE id = %s"""
        cursor["cursor"].execute(query_search,(invoice[4],))
        status = cursor["cursor"].fetchone()
        if invoice:
            return json({"data":{
                    "nro_invoices":invoice[1],
                    "total":invoice[3],
                    "status":status[1],
                    "paid":invoice[6],
                    "date":invoice[9],
                    "deleted":invoice[8]
            },"code":200},200)    
        else:
            return json({"data":"No se consiguio ninguna factura","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def updateInvoice(request):
    try:
        cursor = connectPSQL()
        valid = validInvoice(request)
        if valid == True:
            query = """
                UPDATE invoices set 
                    nro_invoice = %s,
                    id_user = %s,
                    nit = %s,
                    price= %s,
                    iva =%s,
                    sub_total = %s,
                    total = %s,
                WHERE id = %s"""
            records = (request["nro_invoice"],request["id_user"],request["nit"],request["price"],request["iva"],request["sub_total"],request["total"],request["id"],)
            cursor["cursor"].execute(query,records)
            cursor["conn"].commit()
            await updateInvoiceDetail(request)

    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def updateInvoiceUser(request,data):
    try:
        cursor = connectPSQL()
        query = """
            UPDATE invoices set 
                id_user = %s
            WHERE id = %s"""
        records = (request["id_user"],request["id_invoice"],)
        cursor["cursor"].execute(query,records)
        await addNotification({
            "destination":request['id_user'],
            "source":data,
            "description":"Te han asignado la factura #{id}".format(id=request["id_invoice"])})
        cursor["conn"].commit()
        return json({"data":"Usuario asignado con éxito","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

def addInvoiceDetail(request):
    cursor = connectPSQL()
    query_search = """SELECT * from invoices ORDER BY id DESC limit 1"""
    cursor["cursor"].execute(query_search)
    invoice = cursor["cursor"].fetchone()
    for val in request["products"]:
        query_noti = """INSERT INTO invoice_detail (amount,description,quantity,id_invoice) VALUES (%s,%s,%s,%s)"""
        records = (val["amount"],val["description"],int(val["quantity"]),invoice[0],)
        cursor["cursor"].execute(query_noti,records)
        cursor["conn"].commit()

async def updateInvoiceDetail(request):
    try:
        cursor = connectPSQL()
        valid = validInvoice(request)
        if valid == True:
            query = """
                UPDATE invoice_detail set 
                    amount = %s,
                    description = %s,
                    quantity = %s
                WHERE id_invoice = %s"""
            records = (request["amount"],request["description"],request["quantity"],request["id"])
            cursor["cursor"].execute(query,records)
            cursor["conn"].commit()

    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def listInvoices():
    try:
        cursor = connectPSQL()
        invoicesArr = []
        details = []
        query_search = """SELECT * from invoices"""
        cursor["cursor"].execute(query_search)
        invoices = cursor["cursor"].fetchall()
        if invoices:
            for x in invoices:
                query_search = """SELECT * from invoices_status WHERE id = %s"""
                cursor["cursor"].execute(query_search,(x[3],))
                status = cursor["cursor"].fetchone()
                query_search = """SELECT * from invoice_detail WHERE id_invoice = %s"""
                cursor["cursor"].execute(query_search,(x[0],))
                detail = cursor["cursor"].fetchall()
                query_search = """SELECT email from supplier WHERE name = %s"""
                cursor["cursor"].execute(query_search,(x[9],))
                supplier_email = cursor["cursor"].fetchone()
                if x[2] != None:
                    query_search3 = """SELECT * from users where id = %s"""
                    cursor["cursor"].execute(query_search3,(x[2],))
                    user = cursor["cursor"].fetchone()
                    uservalue = user[4]+ " "+user[5]
                else:
                    uservalue = "Sin Asignar"
                for y in detail:
                    details.append({'amount':y[1],'product':y[2],'quantity':y[3]})
                invoicesJson = {
                    "id": x[0],
                    "nro_invoice":x[1],
                    "total":x[11],
                    "user": uservalue,
                    "supplier": x[9],
                    "status":status[1],
                    "date":x[8],
                    "products":details,
                    "supplier_email":supplier_email[0]
                }
                invoicesArr.append(invoicesJson)
                details = []
            return json({"data":invoicesArr,"code":200},200)
        else:
            return json({"data":[],"code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def uploadFile(request):
    try:
        file = request.files.get("file")
        completeName = os.path.join("C:/Users/Usuario/Documents/UiPath/Invoices_Extraction/Invoices", file.name)
        file1 = open(completeName, "wb")
        file1.write(file.body)
        file1.close()
        return json({"data":"Exito","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def listInvoicesRobot():
    try:
        cursor = connectPSQL()
        invoicesArr = []
        details = []
        query_search = """SELECT * from invoices_robot"""
        cursor["cursor"].execute(query_search)
        invoices = cursor["cursor"].fetchall()
        if invoices:
            for x in invoices:
                path = x[5].split("\\")
                query_search = """SELECT * from invoice_detail_robot WHERE id_invoice = %s"""
                cursor["cursor"].execute(query_search,(x[0],))
                detail = cursor["cursor"].fetchall()
                for y in detail:
                    details.append({'amount':y[1],'description':y[2],'quantity':y[4]})
                invoicesJson = {
                    "id": x[0],
                    "nro_invoice":x[1],
                    "total":x[2],
                    "supplier": x[4],
                    "date":x[3],
                    "products":details,
                    "path": path[1]
                }
                invoicesArr.append(invoicesJson)
            return json({"data":invoicesArr,"code":200},200)
        else:
            return json({"data":"No se consiguio ninguna factura","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def delRobotInvoice():
    try:
        cursor = connectPSQL()
        sql_delete_query = """DELETE FROM invoice_detail_robot"""
        cursor["cursor"].execute(sql_delete_query)
        cursor["conn"].commit()
        sql_delete_query = """DELETE FROM invoices_robot"""
        cursor["cursor"].execute(sql_delete_query)
        cursor["conn"].commit()
        return json({"data":"Factura eliminada","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def processInvoice():
    try:
        os.system("C:/Users/Usuario/Desktop/Invoices.bat")
        return json({"data":"Factura Procesada","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)