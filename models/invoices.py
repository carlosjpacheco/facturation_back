from datetime import datetime
import time
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json

async def addInvoice(request,data):
    try:
        cursor = connectPSQL()
        query_noti = """INSERT INTO invoices (nro_invoice,date,id_user,nit,price,iva,sub_total,total,id_status,created_at,id_purchase_order) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        records = (request["nro_invoice"],request["date"],request["id_user"],request["nit"],request["price"],request["iva"],request["subtotal"],request["total"],request["id_status"],datetime.now().timestamp(),request["id_purchase_order"])
        cursor["cursor"].execute(query_noti,records)
        cursor["conn"].commit()
        return json({"data":"Factura creada","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def delInvoice(request):
    try:
        cursor = connectPSQL()
        sql_delete_query = """Update invoices set status=false where id = %s"""
        cursor["cursor"].execute(sql_delete_query, (request["id"],))
        cursor["conn"].commit()
        return json({"data":"Factura eliminada","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

def searchInvoice(request):
    try:
        cursor = connectPSQL()
        query_search = """SELECT * from invoices WHERE id = %s"""
        cursor["cursor"].execute(query_search,(request["id"],))
        invoice = cursor["cursor"].fetchone()
        if invoice:
            return json({"data":invoice,"code":200},200)    
        else:
            return json({"data":"No se consiguio ninguna factura","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)