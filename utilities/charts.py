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
        return json({"data":{"processed":ordersP[0],'unprocessed':orders[0], 'total':orders[0]+ordersP[0]},"code":200},200)
    except (Exception , psycopg2.Error) as error:
        return json({"error":str(error),"code":500})

async def assign_user_purchaseOrder_bar():
    try:
        today =datetime.strptime(str(date.today())+"T23:59:59Z","%Y-%m-%dT%H:%M:%SZ")
        days = []
        week = today - timedelta(days=7)
        cursor = connectPSQL()
        while(week < today):
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
            week = week + timedelta(days=1)
            days.append({"processed":ordersP[0],'unprocessed':orders[0],"date":week})
        return json({"data":days,"code":200},200)
    except (Exception , psycopg2.Error) as error:
        print(error)
        return json({"error":str(error),"code":500})