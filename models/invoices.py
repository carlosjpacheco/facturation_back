from datetime import datetime
import re
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
            query_noti = """INSERT INTO invoices (nro_invoice,id_user,total,id_status,id_purchase_order,paid,created_at,deleted,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            records = (request["nro_invoice"],request["id_user"],request["total"],request["id_status"],request["id_purchase_order"],False,data,False,datetime.strptime(request["date"],"%d/%m/%Y").timestamp(),)
            cursor["cursor"].execute(query_noti,records)
            print("QLQQQ")
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

def addInvoiceDetail(request):
    cursor = connectPSQL()
    query_search = """SELECT * from invoices WHERE nro_invoice = %s"""
    cursor["cursor"].execute(query_search,(request["nro_invoice"],))
    invoice = cursor["cursor"].fetchone()
    query_noti = """INSERT INTO invoice_detail (amount,description,quantity,id_invoice) VALUES (%s,%s,%s,%s)"""
    records = (request["amount"],request["description"],request["quantity"],invoice[0],)
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
                cursor["cursor"].execute(query_search,(x[4],))
                status = cursor["cursor"].fetchone()
                query_search = """SELECT * from invoice_detail WHERE id_invoice = %s"""
                cursor["cursor"].execute(query_search,(x[0],))
                detail = cursor["cursor"].fetchall()
                for y in detail:
                    details.append({'amount':y[1],'product':y[2],'quantity':y[3]})
                invoicesJson = {
                    "nro_invoice":x[1],
                    "total":x[3],
                    "status":status[1],
                    "date":x[9],
                    "products":details
                }
                invoicesArr.append(invoicesJson)
            return json({"data":invoicesArr,"code":200},200)
        else:
            return json({"data":"No se consiguio ninguna factura","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)
