from os import curdir
import re
from sqlite3 import Cursor
from utilities.connections import connectPSQL
from sanic.response import json

async def validSignup(request):
    cursor = connectPSQL()
    if "username" in request:
        username_query= """SELECT * FROM users WHERE username= %s"""
        cursor['cursor'].execute(username_query,(request['username'],))
        if cursor["cursor"].fetchone():
            return json({"error":"Username no disponible","code":500},500)
    if "dni_rif" in request:
        dni_rif_query= """SELECT * FROM users WHERE dni_rif= %s"""
        cursor['cursor'].execute(dni_rif_query,(request['dni_rif'],))
        if cursor["cursor"].fetchone():
            return json({"error":"Ya existe un usuario con el mismo numero de dni_rif","code":500},500)
    if "rif" in request:
        dni_rif_query= """SELECT * FROM supplier WHERE rif= %s"""
        cursor['cursor'].execute(dni_rif_query,(request['rif'],))
        if cursor["cursor"].fetchone():
            return json({"error":"Ya existe un proveedor con el mismo numero de rif","code":500},500)
    return True

async def validUpdateUser(request):

    cursor = connectPSQL()
    user_query = """SELECT * FROM users WHERE id = %s"""
    cursor["cursor"].execute(user_query,(request["id"],))
    user = cursor["cursor"].fetchone()
    if user:
        if "username" in request:
            # if request["username"]==user[1]:
            #     return json({"error":"El nuevo username no puede ser el que ya esta en uso","code":500},500)
            if request["username"]!=user[1]:
                search_user_query = """SELECT * FROM users WHERE username= %s"""
                cursor["cursor"].execute(search_user_query,(request["username"],))
                search_user = cursor["cursor"].fetchone()
                if search_user:
                    return json({"error":"Username no disponible","code":500},500)
    return True

async def validSupplierInfo(request):
    cursor = connectPSQL()
    if "name" in request:
        sql_query = """SELECT * from supplier WHERE name = %s"""
        cursor["cursor"].execute(sql_query,(request["name"],))
        supplier = cursor["cursor"].fetchone()
        if supplier:
            return json({"error":"Ya tiene un proveedor registrado con ese nombre","code":500},500)
    if "rif" in request:
        sql_query = """SELECT * from supplier WHERE rif = %s"""
        cursor["cursor"].execute(sql_query,(request["rif"],))
        supplier = cursor["cursor"].fetchone()
        if supplier:
            return json({"error":"Ya tiene un proveedor registrado con ese rif","code":500},500)
    return True

async def validUpdateSupplier(request):

    cursor = connectPSQL()
    user_query = """SELECT * FROM supplier WHERE id = %s"""
    cursor["cursor"].execute(user_query,(request["id"],))
    supplier = cursor["cursor"].fetchone()
    if supplier:
        if "name" in request:
            if request["name"]!=supplier[1]:
                search_user_query = """SELECT * from supplier WHERE name = %s"""
                cursor["cursor"].execute(search_user_query,(request["name"],))
                search_supplier = cursor["cursor"].fetchone()
                if search_supplier:
                    return json({"error":"Ya hay un proveedor con este nombre","code":500},500)
        if "rif" in request:
            if request["rif"]!=supplier[2]:
                search_user_query = """SELECT * from supplier WHERE rif = %s"""
                cursor["cursor"].execute(search_user_query,(request["rif"],))
                search_supplier = cursor["cursor"].fetchone()
                if search_supplier:
                    return json({"error":"Ya hay un proveedor con este RIF","code":500},500)
    return True

async def validRol(request):
    cursor = connectPSQL()
    sql_query = """SELECT * from role WHERE name = %s"""
    cursor["cursor"].execute(sql_query,(request["name"],))
    user = cursor["cursor"].fetchone()
    if user:
        return json({"error":"Ya tiene un rol registrado con ese nombre","code":500},500)
    return True

async def validInvoice(request):
    cursor = connectPSQL()
    if 'nro_invoice' in request:
        sql_query = """SELECT * from invoices WHERE nro_invoice=%s"""
        cursor["cursor"].execute(sql_query,(request["nro_invoice"],))
        invoice = cursor["cursor"].fetchone()   
        if invoice:
               return json({"error":"Ya tiene una factura agregada con e mismo número de referencia","code":500},500)

    if 'nit' in request:
        sql_query = """SELECT * from invoices WHERE nit=%s"""
        cursor["cursor"].execute(sql_query,(request["nit"],))
        invoice = cursor["cursor"].fetchone()   
        if invoice:
               return json({"error":"Ya tiene una factura agregada con e mismo número de nit","code":500},500)
    return True


async def validPurchaseOrder(request):
    cursor = connectPSQL()
    if 'nro_order' in request:
        sql_query = """SELECT * from purchase_order WHERE nro_order=%s"""
        cursor["cursor"].execute(sql_query,(request["nro_order"],))
        invoice = cursor["cursor"].fetchone()   
        if invoice:
               return json({"error":"Ya tiene una orden de compra agregada con e mismo número de referencia","code":500},500)
    return True

async def validContactInfo(request,data):
    cursor = connectPSQL()
    sql_query = """SELECT * from contact_supplier WHERE email = %s"""
    cursor["cursor"].execute(sql_query,(request["email"],data,))
    contact = cursor["cursor"].fetchone()
    if contact:
        return json({"error":"Ya tiene un contacto registrado con ese email","code":500},500)
    sql_query = """SELECT * from contact_supplier WHERE phone_number = %s"""
    cursor["cursor"].execute(sql_query,(request["phone_number"],data,))
    contact = cursor["cursor"].fetchone()
    if contact:
        return json({"error":"Ya tiene un contacto registrado con ese número","code":500},500)
    return True