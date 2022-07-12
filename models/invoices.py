from datetime import datetime
import os
from models.notifications import addNotification
from utilities.connections import connectPSQL
import psycopg2
import shutil 
from sanic.response import json

from utilities.validators import validInvoice

async def addInvoice(request,data):
    try:
        valid = await validInvoice(request)
        if valid == True:
            cursor = connectPSQL()
            query_search = """SELECT * from invoices WHERE nro_invoice = %s and name_supplier = %s"""
            cursor["cursor"].execute(query_search,(request["nro_invoice"],request["supplier"],))
            invoice = cursor["cursor"].fetchone()
            if invoice:
                return json({"error":"La Factura ya fue procesada","code":500},500)        
            else:
                query_noti = """INSERT INTO invoices (nro_invoice,id_user,total,id_status,id_purchase_order,paid,created_at,deleted,date,name_supplier,paid_at,path,shipping_address,tax,payment_terms,currency,shipping_charges) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                records = (request["nro_invoice"],request["user"],float(request["total"]),1,request["id_purchase_order"],False,(datetime.now()).timestamp(),False,request["date"],request["supplier"],None,request["path"],request["shipping_address"],request["tax"],request["payment_terms"],request["currency"],request["shipping_charges"],)
                cursor["cursor"].execute(query_noti,records)
                
                # query_search = """SELECT id from users WHERE first_name = %s"""
                # cursor["cursor"].execute(query_search,(request["supplier"],))
                # user = cursor["cursor"].fetchone()


                query_search = """SELECT id from users WHERE id_role = 2 or first_name = %s"""
                cursor["cursor"].execute(query_search,(request['supplier'],))
                destination = cursor["cursor"].fetchall()
                

                query_history = """INSERT INTO operation_history (description, id_user, date) VALUES (%s,%s,%s)"""
                records_history = ('Se le asigno una factura a la Orden de Compra #'+request["id_purchase_order"],data,datetime.now(),)
                cursor["cursor"].execute(query_history,records_history)
                cursor["conn"].commit()

                addInvoiceDetail(request)
                for x in destination:
                    if x != data:
                        addNotification({
                            'destination':x,
                            'source':data,
                            'description':'Se proceso la factura número {id}'.format(id=request['nro_invoice'])
                        })
                shutil.move("C:/Users/Usuario/Desktop/Angular 13-Tesis/material/src/assets/RobotInvoices/"+request["path"],"C:/Users/Usuario/Desktop/Angular 13-Tesis/material/src/assets/Invoices")
                return json({"data":"Factura creada","code":200},200)
        else:
            return valid
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def delInvoice(request):
    try:
        cursor = connectPSQL()

        sql_delete_query = """SELECT id,path FROM invoices where id_purchase_order = %s"""
        cursor["cursor"].execute(sql_delete_query, (request["id"],))
        invoice = cursor["cursor"].fetchone()

        sql_delete_query1 = """DELETE FROM invoice_detail where id_invoice = %s"""
        cursor["cursor"].execute(sql_delete_query1, (invoice[0],))

        sql_delete_query2 = """DELETE FROM invoices where id = %s"""
        cursor["cursor"].execute(sql_delete_query2, (invoice[0],))

        cursor["conn"].commit()
        os.remove("C:/Users/Usuario/Desktop/Angular 13-Tesis/material/src/assets/Invoices/"+invoice[1])
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

async def listInvoices(request,data):
    try:
        cursor = connectPSQL()
        invoicesArr = []
        details = []
        if request['start_date'] == '':
            if request['role'] == 1 or request['role'] == 4:
                query_search = """SELECT * from invoices"""
                cursor["cursor"].execute(query_search)
                invoices = cursor["cursor"].fetchall()
            elif request['role'] == 10:
                query_search = """SELECT first_name from users WHERE id = %s"""
                cursor["cursor"].execute(query_search,(data,))
                user = cursor["cursor"].fetchone()
                if user:
                    query_search = """SELECT * from invoices where name_supplier = %s"""
                    cursor["cursor"].execute(query_search,(user[0],))
                    invoices = cursor["cursor"].fetchall()
            else:
                query_search = """SELECT * from invoices where id_user = %s order by created_at desc"""
                cursor["cursor"].execute(query_search,(request['id_user'],))
                invoices = cursor["cursor"].fetchall()
        else:
            start_date = datetime.strptime(request['start_date'][:10]+'T00:00:00Z',"%Y-%m-%dT%H:%M:%SZ")
            end_date = datetime.strptime(request['end_date'][:10]+'T23:59:59Z',"%Y-%m-%dT%H:%M:%SZ")
            if request['role'] == 1 or request['role'] == 4:
                query_search = """SELECT * from invoices WHERE created_at >= %s AND created_at<=%s"""
                cursor["cursor"].execute(query_search,(start_date.timestamp(),end_date.timestamp()))
                invoices = cursor["cursor"].fetchall()
            else:
                query_search = """SELECT * from invoices where id_user = %s order and created_at >= %s AND created_at<=%s by created_at desc"""
                cursor["cursor"].execute(query_search,(request['id_user'],start_date.timestamp(),end_date.timestamp()))
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
                    "date":x[6],
                    "products":details,
                    "supplier_email":supplier_email[0],
                    "path": x[12],
                    "id_purchase_order":x[4]
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
        completeName1 = os.path.join("C:/Users/Usuario/Desktop/Angular 13-Tesis/material/src/assets/RobotInvoices/", file.name)
        file1 = open(completeName, "wb")
        file1.write(file.body)
        file1.close()
        file2 = open(completeName1, "wb")
        file2.write(file.body)
        file2.close()
        return json({"data":"Exito","path":file.name,"code":200},200)
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
                    "shipping_address":x[6],
                    "tax":x[7],
                    "payment_terms":x[8],
                    "currency":x[9],
                    "shipping_charges":x[10],                    
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

async def deleteRobotInvoicePDF(request):
    try:
        completeName1 = os.path.join("C:/Users/Usuario/Desktop/Angular 13-Tesis/material/src/assets/RobotInvoices/", request["path"])
        completeName = os.path.join("C:/Users/Usuario/Documents/UiPath/Invoices_Extraction/Invoices", request["path"])
        os.remove(completeName1)
        os.remove(completeName)
        return json({"data":"PDF Eliminado","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def selectItems():
    try:
        itemsArr = []
        cursor= connectPSQL()
        query = """SELECT id, item, status FROM invoice_items order by id asc"""
        cursor['cursor'].execute(query)
        items = cursor['cursor'].fetchall()
        for x in items:
            jsonItem = {
                "id":x[0],
                'item':x[1],
                'status':x[2]
            }
            itemsArr.append(jsonItem)
        return json({"data":itemsArr,'code':200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def disableOrenableItem(request):
    try:
        cursor = connectPSQL()
        if request["status"] == True:
            status = False
            sql_delete_query = """Update invoice_items set status=%s where id = %s"""
            cursor["cursor"].execute(sql_delete_query, (status,request["id"]))
        else:
            status = True
        sql_delete_query = """Update invoice_items set status=%s where id = %s"""
        cursor["cursor"].execute(sql_delete_query, (status,request["id"]))
        cursor["conn"].commit()
        return json({"data":"Item Modificado","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def rejectInvoice(request,data):
    try:
        cursor = connectPSQL()
        
        query = """
            UPDATE invoices set 
                id_status = 2
                WHERE nro_invoice = %s"""
        records = (request["id"],)
        cursor["cursor"].execute(query,records)

        if request["user"] == None:
        
            query_search = """SELECT id from users WHERE first_name = %s"""
            cursor["cursor"].execute(query_search,(request["supplier"],))
            user = cursor["cursor"].fetchone()
            process_user = user[0]
        else:
            process_user = request["user"]
        
        await addNotification({
            "destination":process_user,
            "source":data,
            "description":"Se ha rechazado la factura #{id}".format(id=request["id"])})
        cursor["conn"].commit()
        return json({"data":"Factura rechazada con éxito","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)