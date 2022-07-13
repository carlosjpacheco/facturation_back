from datetime import datetime
import time
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json

from utilities.validators import validPurchaseOrder
from utilities.pdf import pdfPurchaseOrder
from models.notifications import addNotification

async def addPurchaseOrder(request,data):
    try:
        valid = await validPurchaseOrder(request)
        if valid == True:
            cursor = connectPSQL()
            if request["preview"] == False:
                query_noti = """INSERT INTO purchase_order (date,completed,deleted,id_supplier,terms_conditions,delivery_address,id_currency,path) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
                records = (datetime.strptime(request["date"],"%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),False,False,request["supplier"],request["terms_conditions"],request["delivery_address"],request["currency"],'',)
                cursor["cursor"].execute(query_noti,records)
                cursor["conn"].commit()

                await addPurchaseOrderDetail(request,data)
                                        
                query_search = """SELECT name from supplier WHERE id = %s"""
                cursor["cursor"].execute(query_search,(request["supplier"],))
                supplier = cursor["cursor"].fetchone()

                query_search = """SELECT * from users WHERE first_name = %s"""
                cursor["cursor"].execute(query_search,(supplier[0],))
                user_sup = cursor["cursor"].fetchone()

                await addNotification({"destination":user_sup[0],
                                        "source":data,
                                        "description":"Te han han enviado una orden de compra, revisa tu correo"})

                # query_search = """SELECT id from users WHERE id = %s"""
                # cursor["cursor"].execute(query_search,(data,))
                # user = cursor["cursor"].fetchone()

                query_history = """INSERT INTO operation_history (description, id_user, date) VALUES (%s,%s,%s)"""
                records_history = ('Se le asigno una Nueva Orden de Compra',user_sup[0],datetime.now(),)
                cursor["cursor"].execute(query_history,records_history)

                query_history = """INSERT INTO operation_history (description, id_user, date) VALUES (%s,%s,%s)"""
                records_history = ('Generó una Nueva Orden de Compra',request["user_created"],datetime.now(),)
                cursor["cursor"].execute(query_history,records_history)
                cursor["conn"].commit()
                return json({"data":"Orden de compra creada","code":200,"pdf":1},200)
            else:
                return await pdfPurchaseOrder(request,data)
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
        if purchaseOrder:
            query_search2 = """SELECT * from detail_purchase_order WHERE id_purchase_order = %s"""
            cursor["cursor"].execute(query_search2,(request["id"],))
            detailPurchaseOrder = cursor["cursor"].fetchone()
    
            query = """SELECT * from supplier WHERE id = %s"""
            cursor["cursor"].execute(query,(purchaseOrder[4],))
            supp = cursor["cursor"].fetchone()
            for x in detailPurchaseOrder[2]:
                products = {
                    "product":x[0][1:-1],
                    "description":x[1][1:-1],
                    "amount":x[2]
                }
                product.append(products)
        
            return json({"data":{
                "nro_order":purchaseOrder[0],
                "created_at":detailPurchaseOrder[3],
                "completed":purchaseOrder[2],
                "supplier":supp[1],
                "user":purchaseOrder[1],
                "email":supp[5],
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
        val['description']= val['description'].replace(',','|')
        list_val.append(val["name"].capitalize())
        list_val.append(val["description"].capitalize())
        list_val.append(val["quantity"])
        products_list.append(list_val)
    request["products"]= products_list
    
    products = str(products_list)
    products = products.replace("[","{")
    products= products.replace("]","}")
    
    cursor = connectPSQL()
    
    query_search = """SELECT * from purchase_order ORDER BY id DESC limit 1"""
    cursor["cursor"].execute(query_search)
    purchaseOrder = cursor["cursor"].fetchone()
    request["nro_order"] = purchaseOrder[0]

    await pdfPurchaseOrder(request,data)

    path = f"ORD_nro_{purchaseOrder[0]}.pdf"

    sql_update = """Update purchase_order set path=%s where id = %s"""
    cursor["cursor"].execute(sql_update,(path,purchaseOrder[0],))
    query_noti = """INSERT INTO detail_purchase_order (id_purchase_order,created_at,products) VALUES (%s,%s,%s)"""
    records = (purchaseOrder[0],datetime.strptime(request["date"],"%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),products,)
    cursor["cursor"].execute(query_noti,records)

    cursor["conn"].commit()

async def updatePurchaseOrder(request,data):
    try:
        cursor = connectPSQL()
        query = """
            UPDATE purchase_order set 
                id_user = %s
            WHERE id = %s"""
        records = (request["id_user"],request["id_order"],)
        cursor["cursor"].execute(query,records)
        if (data != request['id_user']):
            await addNotification({
                "destination":request['id_user'],
                "source":data,
                "description":"Te han asignado la orden de compra #{id}".format(id=request["id_order"])})
        cursor["conn"].commit()
        return json({"data":"Usuario asignado con éxito","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def listPurchaseOrder(request,data):
    try:
        cursor = connectPSQL()
        purchaseOrdersArr = []

        if request['start_date'] == '':
            if request['role'] == 1 or request['role'] == 2:
                query_search = """SELECT * from purchase_order order by id desc"""
                cursor["cursor"].execute(query_search)
                purchaseOrders = cursor["cursor"].fetchall()
            elif request['role'] == 10:
                query_search = """SELECT first_name from users WHERE id = %s"""
                cursor["cursor"].execute(query_search,(data,))
                user = cursor["cursor"].fetchone()
                if user:
                    query_search = """SELECT id from supplier WHERE name = %s"""
                    cursor["cursor"].execute(query_search,(user[0],))
                    supplier = cursor["cursor"].fetchone()

                    if supplier:
                        query_search = """SELECT * from purchase_order WHERE id_supplier = %s order by id desc"""
                        cursor["cursor"].execute(query_search,(supplier[0],))
                        purchaseOrders = cursor["cursor"].fetchall()
            else:
                query_search = """SELECT * from purchase_order where id_user = %s order by id desc"""
                cursor["cursor"].execute(query_search,(request['id_user'],))
                purchaseOrders = cursor["cursor"].fetchall()
        else:
            start_date = datetime.strptime(request['start_date'][:10]+'T00:00:00Z',"%Y-%m-%dT%H:%M:%SZ")
            end_date = datetime.strptime(request['end_date'][:10]+'T23:59:59Z',"%Y-%m-%dT%H:%M:%SZ")
            if request['role'] == 1 or request['role'] == 2:
                query_search = """SELECT * from purchase_order where date>= %s and date <=%s order by id desc"""
                cursor["cursor"].execute(query_search,(start_date.timestamp(),end_date.timestamp()))
                purchaseOrders = cursor["cursor"].fetchall()
            else:
                query_search = """SELECT * from purchase_order where id_user = %s and date>= %s and date <=%s order by id desc"""
                cursor["cursor"].execute(query_search,(request['id_user'],start_date.timestamp(),end_date.timestamp()))
                purchaseOrders = cursor["cursor"].fetchall()

        if purchaseOrders:
            for x in purchaseOrders:
                query_search = """SELECT * from detail_purchase_order where id_purchase_order = %s"""
                cursor["cursor"].execute(query_search,(x[0],))
                query_search2 = """SELECT * from supplier where id = %s"""
                cursor["cursor"].execute(query_search2,(x[4],))
                supplier = cursor["cursor"].fetchone()
                query_search3 = """SELECT * from invoices where id_purchase_order = %s"""
                cursor["cursor"].execute(query_search3,(x[0],))
                con_factura = cursor["cursor"].fetchone()
                factura = True if con_factura else False
                path_factura = con_factura[12] if factura else " "
                status_factura = con_factura[3] if factura else 0
                usuario_pagar = con_factura[2] if factura else None
                if x[1] != None:
                    query_search3 = """SELECT * from users where id = %s"""
                    cursor["cursor"].execute(query_search3,(x[1],))
                    user = cursor["cursor"].fetchone()
                    uservalue = user[4]+ " "+user[5]
                else:
                    uservalue = "Sin Asignar"
                
                purchaseOrdersJson = {
                    "nro_order":x[0],
                    "date":x[9],
                    "user": uservalue,
                    "supplier":supplier[1],
                    "path": x[8],
                    "factura": factura,
                    "path_factura": path_factura,
                    "status_factura": status_factura,
                    "usuario_pagar": usuario_pagar
                } 
                purchaseOrdersArr.append(purchaseOrdersJson)
            return json({"data":{"purchaseOrders":purchaseOrdersArr,"code":200}},200)
        else:
            return json({"data":[],"code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":error,"code":500},500)

async def listCurrency():
    try:
        currencyArr = []
        cursor = connectPSQL()
        query_search = """SELECT * from currency WHERE id = 1"""
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

async def selectProducts():
    try:
        product=[]
        cursor = connectPSQL()
        query = """SELECT products from detail_purchase_order"""
        cursor['cursor'].execute(query)
        products = cursor['cursor'].fetchall()
        for x in products:
            prod=x[0][0][0][1:-1]
            if prod not in product:
                product.append(prod)
        return json({"data":product,"code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({'error':str(error),'code':500},500)