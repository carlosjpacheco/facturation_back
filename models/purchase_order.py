from datetime import datetime
from importlib.resources import path
from locale import currency
import time
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json

from utilities.validators import validPurchaseOrder
from utilities.pdf import pdfPurchaseOrder

async def addPurchaseOrder(request,data):
    try:
        valid = await validPurchaseOrder(request)
        if valid == True:
            cursor = connectPSQL()
            if request["preview"] == False:
                query_noti = """INSERT INTO purchase_order (id_user,date,completed,deleted,id_supplier,terms_conditions,delivery_address,id_currency,path) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                records = (request["id_user"],datetime.strptime(request["date"],"%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),False,False,request["supplier"],request["terms_conditions"],request["delivery_address"],request["currency"],'',)
                cursor["cursor"].execute(query_noti,records)
                cursor["conn"].commit()
                await addPurchaseOrderDetail(request,data)
                return json({"data":"Orden de compra creada","code":200},200)
            else:
                await pdfPurchaseOrder(request,data)
                return json({"data":"ok","code":200},200)
        else:
            return valid
    except (Exception, psycopg2.Error) as error:
        return json({"error":error,"code":500},500)

async def delpurchaseOrder(request):
    try:
        cursor = connectPSQL()
        sql_delete_query = """Update purchase_order set deleted=true where id = %s"""
        cursor["cursor"].execute(sql_delete_query, (request["id"],))
        cursor["conn"].commit()
        return json({"data":"Orden de compra eliminada","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def readPurchaseOrder(request):
    try:
        product=[]
        cursor = connectPSQL()
        query_search = """SELECT * from purchase_order WHERE id = %s"""
        cursor["cursor"].execute(query_search,(request["id"],))
        purchaseOrder = cursor["cursor"].fetchone()
        query_search2 = """SELECT * from detail_purchase_order WHERE id_purchase_order = %s"""
        cursor["cursor"].execute(query_search2,(request["id"],))
        detailPurchaseOrder = cursor["cursor"].fetchone()
        if purchaseOrder:
            for x in detailPurchaseOrder[3]:
                products = {
                    "product":x[0],
                    "description":x[1],
                    "amount":x[2]
                }
                product.append(products)
            return json({"data":{
                "nro_order":purchaseOrder[1],
                "created_at":detailPurchaseOrder[2],
                "products":product
            },"code":200},200)    
        else:
            return json({"data":"No se consiguio ninguna orden de compra","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def addPurchaseOrderDetail(request,data):
    products_list = []
    for val in request["products"]:
        list_val = []
        list_val.append(val["name"])
        list_val.append(val["description"])
        list_val.append(val["quantity"])
        products_list.append(list_val)
    
    products = str(products_list)  
    products = products.replace("[","{")
    products= products.replace("]","}")
    
    cursor = connectPSQL()
    
    query_search = """SELECT * from purchase_order ORDER BY id DESC limit 1"""
    cursor["cursor"].execute(query_search)
    purchaseOrder = cursor["cursor"].fetchone()
    request["nro_order"] = purchaseOrder[0]

    request["products"]= products_list
    await pdfPurchaseOrder(request,data)

    path = f"ORD_Nro{purchaseOrder[0]}"

    sql_update = """Update purchase_order set path=%s where id = %s"""
    cursor["cursor"].execute(sql_update,(path,purchaseOrder[0],))
    
    query_noti = """INSERT INTO detail_purchase_order (id_purchase_order,created_at,products) VALUES (%s,%s,%s)"""
    records = (purchaseOrder[0],datetime.strptime(request["date"],"%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),products,)
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


async def listPurchaseOrder():
    try:
        cursor = connectPSQL()
        purchaseOrdersArr = []
        query_search = """SELECT * from purchase_order"""
        cursor["cursor"].execute(query_search)
        purchaseOrders = cursor["cursor"].fetchall()
        if purchaseOrders:
            for x in purchaseOrders:
                query_search = """SELECT * from detail_purchase_order where id_purchase_order = %s"""
                cursor["cursor"].execute(query_search,(x[0],))
                query_search2 = """SELECT * from supplier where id = %s"""
                cursor["cursor"].execute(query_search2,(x[5],))
                supplier = cursor["cursor"].fetchone()
                purchaseOrdersJson = {
                    "nro_order":x[1],
                    "date":x[2],
                    "supplier":supplier[1],
                    "ruta": x[8]
                } 
                purchaseOrdersArr.append(purchaseOrdersJson)
            return json({"data":{"purchaseOrders":purchaseOrdersArr,"code":200}},200)
        else:
            return json({"data":"No se consiguio ninguna orden de compra","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":error,"code":500},500)

async def listCurrency():
    try:
        currencyArr = []
        cursor = connectPSQL()
        query_search = """SELECT * from currency"""
        cursor["cursor"].execute(query_search)
        currency = cursor["cursor"].fetchall()
        for x in currency:
            currencyJson = {
                "id":x[0],
                "name": x[1]
            }
            currencyArr.append(currencyJson)
        return json({"data":currencyArr,"code":200},200)
    except (Exception,psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)