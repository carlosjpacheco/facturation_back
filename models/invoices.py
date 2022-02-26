from datetime import datetime
import time
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json

from utilities.validators import validInvoice

async def addInvoice(request,data):
    try:
        valid = await validInvoice(request)
        if valid == True:
            cursor = connectPSQL()
            query_noti = """INSERT INTO invoices (nro_invoice,date,id_user,nit,price,iva,sub_total,total,id_status,created_at,id_purchase_order,paid,created_by) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            records = (request["nro_invoice"],datetime.strptime(request["date"],"%d/%m/%Y").timestamp(),request["id_user"],request["nit"],request["price"],request["iva"],request["sub_total"],request["total"],request["id_status"],datetime.now().timestamp(),request["id_purchase_order"],False,data,)
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

async def searchInvoice(request):
    try:
        cursor = connectPSQL()
        query_search = """SELECT * from invoices WHERE id = %s"""
        cursor["cursor"].execute(query_search,(request["id"],))
        invoice = cursor["cursor"].fetchone()
        if invoice:
            return json({"data":{
                "nro_invoice":invoice[1],
                "nit":invoice[3],
                "price":float(invoice[4]),
                "iva":float(invoice[5]),
                "sub_total":float(invoice[6]),
                "total":float(invoice[7]),
                "status":invoice[8],
                "paid":invoice[10],
                "date":invoice[11],
                "deleted":invoice[14]
            },"code":200},200)    
        else:
            return json({"data":"No se consiguio ninguna factura","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

# async def updateInvoice(request):
#     try:
#         cursor = connectPSQL()
#         valid = validInvoice(request)
#         if valid == True:
            
#     except (Exception, psycopg2.Error) as error:
#         return json({"error":str(error),"code":500},500)

def addInvoiceDetail(request):
    cursor = connectPSQL()
    query_search = """SELECT * from invoices WHERE nro_invoice = %s"""
    cursor["cursor"].execute(query_search,(request["nro_invoice"],))
    invoice = cursor["cursor"].fetchone()
    query_noti = """INSERT INTO invoice_detail (amount,description,quantity,id_invoice,created_at) VALUES (%s,%s,%s,%s,%s)"""
    records = (request["amount"],request["description"],request["quantity"],invoice[0],datetime.now().timestamp(),)
    cursor["cursor"].execute(query_noti,records)
    cursor["conn"].commit()