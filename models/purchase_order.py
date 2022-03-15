from datetime import datetime
import time
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json

from utilities.validators import validPurchaseOrder

async def addPurchaseOrder(request,data):
    try:
        valid = await validPurchaseOrder(request)
        if valid == True:
            cursor = connectPSQL()
            query_noti = """INSERT INTO purchase_order (nro_order,id_user,date,completed,active) VALUES (%s,%s,%s)"""
            records = (request["nro_order"],request["id_user"],datetime.strptime(request["date"],"%d/%m/%Y").timestamp(),False,True)
            cursor["cursor"].execute(query_noti,records)
            cursor["conn"].commit()
            addPurchaseOrderDetail(request)
            return json({"data":"Orden de compra creada","code":200},200)
        else:
            return valid
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def delpurchaseOrder(request):
    try:
        cursor = connectPSQL()
        sql_delete_query = """Update purchase_order set deleted=true where id = %s"""
        cursor["cursor"].execute(sql_delete_query, (request["id"],))
        cursor["conn"].commit()
        return json({"data":"Orden de compra eliminada","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def searchpurchaseOrder(request):
    try:
        cursor = connectPSQL()
        cursor2 = connectPSQL()
        query_search = """SELECT * from purchase_order WHERE id = %s"""
        query_search2 = """SELECT * from detail_purchase_order WHERE id_purchase_order = %s"""
        cursor["cursor"].execute(query_search,(request["id"],))
        cursor2["cursor"].execute(query_search2,(request["id"],))
        purchaseOrder = cursor["cursor"].fetchone()
        detailPurchaseOrder = cursor2["cursor"].fetchone()
        if purchaseOrder:
            return json({"data":{
                "nro_order":purchaseOrder[1],
                "quantity":detailPurchaseOrder[1],
                "description":detailPurchaseOrder[2],
                "created_at":detailPurchaseOrder[3]
            },"code":200},200)    
        else:
            return json({"data":"No se consiguio ninguna orden de compra","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

def addPurchaseOrderDetail(request):
    cursor = connectPSQL()
    query_search = """SELECT * from purchase_order WHERE nro_order = %s"""
    cursor["cursor"].execute(query_search,(request["nro_purchaseOrder"],))
    purchaseOrder = cursor["cursor"].fetchone()
    query_noti = """INSERT INTO purchase)order (quantity,description,created_at,id_purchase_order) VALUES (%s,%s,%s,%s)"""
    records = (request["quantity"],request["description"],datetime.strptime(request["date"],"%d/%m/%Y").timestamp(),purchaseOrder[0])
    cursor["cursor"].execute(query_noti,records)
    cursor["conn"].commit()

async def updatePurchaseOrder(request):
    try:
        cursor = connectPSQL()
        valid = validPurchaseOrder(request)
        if valid == True:
            query = """
                UPDATE invoices set 
                    nro_order = %s,
                    id_user = %s
                WHERE id = %s"""
            records = (request["nro_order"],request["id_user"],)
            cursor["cursor"].execute(query,records)
            cursor["conn"].commit()
            await updatePurchaseOrderDetail(request)

    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)


async def updatePurchaseOrderDetail(request):
    try:
        cursor = connectPSQL()
        valid = validPurchaseOrder(request)
        if valid == True:
            query = """
                UPDATE detail_purchase_order set 
                    quantity = %s,
                    description = %s
                WHERE id_purchase_order = %s"""
            records = (request["quantity"],request["description"],request["id"],)
            cursor["cursor"].execute(query,records)
            cursor["conn"].commit()

    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)


# Falta listar