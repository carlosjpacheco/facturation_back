from datetime import datetime,date, timedelta
import time
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json

async def assign_user_purchaseOrder_pie():
    try:
        cursor = connectPSQL()
        query_search = """SELECT COUNT(ord.id)
                            from purchase_order ord WHERE
                            ord.id not in (SELECT id_purchase_order
                            FROM invoices); """
        cursor["cursor"].execute(query_search)
        orders = cursor["cursor"].fetchone()
        query_search = """SELECT COUNT(ord.id)
                            from purchase_order ord WHERE
                            ord.id in (SELECT id_purchase_order
                            FROM invoices); """
        cursor["cursor"].execute(query_search)
        ordersP = cursor["cursor"].fetchone()
        return json({"data":{"processed":ordersP[0],'unProcessed':orders[0], 'total':orders[0]+ordersP[0]},"code":200},200)
    except (Exception , psycopg2.Error) as error:
        return json({"error":str(error),"code":500})

async def assign_user_purchaseOrder_bar():
    try:
        today =datetime.strptime(str(date.today())+"T23:59:59Z","%Y-%m-%dT%H:%M:%SZ")
        days = []
        processed = []
        unProcessed = []
        week = today - timedelta(days=6)
        cursor = connectPSQL()
        while(week <= today):
            query_search = """SELECT COUNT(ord.id)
                                from purchase_order ord WHERE
                                ord.id not in (SELECT id_purchase_order
                                FROM invoices) and 
                                date >= %s and date <= %s;"""
            cursor["cursor"].execute(query_search,(week.timestamp(),(week + timedelta(days=1)).timestamp()))
            orders = cursor["cursor"].fetchone()
            query_search = """SELECT COUNT(ord.id)
                                from purchase_order ord WHERE
                                ord.id in (SELECT id_purchase_order
                                FROM invoices) and
                                date >= %s and date <= %s;"""
            cursor["cursor"].execute(query_search,(week.timestamp(),(week + timedelta(days=1)).timestamp()))
            ordersP = cursor["cursor"].fetchone()
            days.append(str(week)[5:10])
            processed.append(ordersP[0])
            unProcessed.append(orders[0])
            week = week + timedelta(days=1)
        return json({"data":{'days':days,'processed':processed,'unProcessed':unProcessed},"code":200},200)
    except (Exception , psycopg2.Error) as error:
        return json({"error":str(error),"code":500})

async def pay_invoice_pie():
    try:
        cursor = connectPSQL()
        query_search = """SELECT COUNT(inv.id)
                            from invoices inv WHERE
                            inv.id_status = 1;"""
        cursor["cursor"].execute(query_search)
        invoice = cursor["cursor"].fetchone()
        query_search = """SELECT COUNT(inv.id)
                            from invoices inv WHERE
                            inv.id_status = 0;"""
        cursor["cursor"].execute(query_search)
        invoiceP = cursor["cursor"].fetchone()
        return json({"data":{"invoice":invoiceP[0],'invoiceP':invoice[0], 'total':invoice[0]+invoiceP[0]},"code":200},200)
    except (Exception , psycopg2.Error) as error:
        return json({"error":str(error),"code":500})

async def pay_invoice_bar():
    try:
        today =datetime.strptime(str(date.today())+"T23:59:59Z","%Y-%m-%dT%H:%M:%SZ")
        days = []
        processed = []
        unProcessed = []
        week = today - timedelta(days=6)
        cursor = connectPSQL()
        while(week <= today):
            query_search = """SELECT COUNT(ord.id)
                            from invoices inv WHERE
                            inv.id_status = 0
                            paid_at >= %s and paid_at <= %s;"""
            cursor["cursor"].execute(query_search,(week.timestamp(),(week + timedelta(days=1)).timestamp()))
            orders = cursor["cursor"].fetchone()
            query_search = """SELECT COUNT(ord.id)
                            from invoices inv WHERE
                            inv.id_status = False
                            paid_at >= %s and paid_at <= %s;"""
            cursor["cursor"].execute(query_search,(week.timestamp(),(week + timedelta(days=1)).timestamp()))
            ordersP = cursor["cursor"].fetchone()
            days.append(str(week)[5:10])
            processed.append(ordersP[0])
            unProcessed.append(orders[0])
            week = week + timedelta(days=1)
        return json({"data":{'days':days,'processed':processed,'unProcessed':unProcessed},"code":200},200)
    except (Exception , psycopg2.Error) as error:
        return json({"error":str(error),"code":500})

async def assign_user_purchaseOrder_line():
    try:
        cursor = connectPSQL()
        query = """SELECT * FROM users WHERE id_role = 3"""
        cursor['cursor'].execute(query)
        users = cursor['cursor'].fetchall()
        datasets = []
        for x in users:
            today =datetime.strptime(str(date.today())+"T23:59:59Z","%Y-%m-%dT%H:%M:%SZ")
            week = today - timedelta(days=6)
            days = []
            amounts = []
            while(week <= today):
                
                query = """SELECT count(id) FROM purchase_order
                        WHERE id_user = %s and
                        date >= %s and date <= %s"""
                records = (x[0],week.timestamp(),(week + timedelta(days=1)).timestamp())
                cursor['cursor'].execute(query,records)
                count = cursor['cursor'].fetchone()
                amounts.append(count[0])
                days.append(str(week)[5:10])
                week = week + timedelta(days=1)
            names = x[4].split(' ')
            names = names[0]
            last = x[5].split(' ')
            last = last[0][:1]
            data = {
                'data':amounts,'label':names+ ' '+last+'.'
            }
            datasets.append(data)
        return json({"data":{'datasets':datasets,'days':days},"code":200},200)
    except (Exception , psycopg2.Error) as error:
        return json({"error":str(error),"code":500})

async def assign_user_invoices_line():
    try:
        cursor = connectPSQL()
        query = """SELECT * FROM users WHERE id_role = 5"""
        cursor['cursor'].execute(query)
        users = cursor['cursor'].fetchall()
        datasets = []
        for x in users:
            today =datetime.strptime(str(date.today())+"T23:59:59Z","%Y-%m-%dT%H:%M:%SZ")
            week = today - timedelta(days=6)
            days = []
            amounts = []
            while(week <= today):
                
                query = """SELECT count(id) FROM invoices
                        WHERE id_user = %s and
                        created_at >= %s and created_at <= %s"""
                records = (x[0],week.timestamp(),(week + timedelta(days=1)).timestamp())
                cursor['cursor'].execute(query,records)
                count = cursor['cursor'].fetchone()
                amounts.append(count[0])
                days.append(str(week)[5:10])
                week = week + timedelta(days=1)
            names = x[4].split(' ')
            names = names[0]
            last = x[5].split(' ')
            last = last[0][:1]
            data = {
                'data':amounts,'label':names+ ' '+last+'.'
            }
            datasets.append(data)
        return json({"data":{'datasets':datasets,'days':days},"code":200},200)
    except (Exception , psycopg2.Error) as error:
        return json({"error":str(error),"code":500})
