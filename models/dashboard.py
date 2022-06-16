from calendar import month
from datetime import date, datetime, timedelta
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json

########################### Summary of the day ################################################
async def amount_paid_in_invoices_daily():
    try:
        cursor = connectPSQL()
        today = today =datetime.strptime(str(date.today())+"T00:00:01Z","%Y-%m-%dT%H:%M:%SZ")
        query = """
            select po.id_currency, SUM(inv.total), count(inv.id)
            from invoices inv , purchase_order po
            where inv.paid_at >= %s
            and inv.id_purchase_order = po.id
            group by po.id_currency,inv.id
        """
        records = (today.timestamp(),)
        cursor['cursor'].execute(query,records)
        data = cursor['cursor'].fetchall()
        print('1!!!!!!!!!!!!!',data)
        return json({'data':data,'code':200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def count_invoices_daily():
    try:
        cursor = connectPSQL()
        today = today =datetime.strptime(str(date.today())+"T00:00:01Z","%Y-%m-%dT%H:%M:%SZ")
        query = """
        select count(id)
        from invoices 
        where created_at >=%s
        """
        records = (today.timestamp(),)
        cursor['cursor'].execute(query,records)
        data = cursor['cursor'].fetchone()
        print('2!!!!!',data[0])

        return json({'data':data[0],'code':200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def count_pro_unpro_daily():
    try:
        cursor = connectPSQL()
        today = today =datetime.strptime(str(date.today())+"T00:00:01Z","%Y-%m-%dT%H:%M:%SZ")
        query = """
            select count(po.id),po.completed
            from purchase_order po
            where completed_at >= %s or date >= %s
            group by po.completed
			order by po.completed desc
        """
        records = (today.timestamp(),today.timestamp(),)
        cursor['cursor'].execute(query,records)
        data = cursor['cursor'].fetchall()
        print('3!!!!!!!',data)

        return json({'data':data,'code':200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)
        
########################### Summary last 15 days ################################################

async def amount_paid_in_invoices_lastDay():
    try:
        cursor = connectPSQL()
        today = today =datetime.strptime(str(date.today())+"T00:00:01Z","%Y-%m-%dT%H:%M:%SZ")
        today = today - timedelta(days=14)
        query = """
            select po.id_currency, SUM(inv.total), count(inv.id)
            from invoices inv , purchase_order po
            where inv.paid_at >= %s
            and inv.id_purchase_order = po.id
            group by po.id_currency,inv.id
        """
        records = (today.timestamp(),)
        cursor['cursor'].execute(query,records)
        data = cursor['cursor'].fetchall()
        print('4!!!!!!!!!',data)
        return json({'data':data,'code':200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def count_invoices_lastDays():
    try:
        cursor = connectPSQL()
        today = today =datetime.strptime(str(date.today())+"T00:00:01Z","%Y-%m-%dT%H:%M:%SZ")
        today = today - timedelta(days=14)
        query = """
        select count(id)
        from invoices 
        where created_at >=%s
        """
        records = (today.timestamp(),)
        cursor['cursor'].execute(query,records)
        data = cursor['cursor'].fetchone()
        print('5!!!!!!!!',data)

        return json({'data':data[0],'code':200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def count_pro_unpro_LastDays():
    try:
        cursor = connectPSQL()
        today = today =datetime.strptime(str(date.today())+"T00:00:01Z","%Y-%m-%dT%H:%M:%SZ")
        today = today - timedelta(days=14)
        query = """
            select count(po.id),po.completed
            from purchase_order po
            where completed_at >= %s or date >= %s
            group by po.completed
			order by po.completed desc
        """
        records = (today.timestamp(),today.timestamp(),)
        cursor['cursor'].execute(query,records)
        data = cursor['cursor'].fetchall()
        print('6!!!!!!!',data)

        return json({'data':data,'code':200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

########################### Summary last 15 days ################################################


async def top_supplier_by_TotalInv():
    try:
        cursor = connectPSQL()
        today = today =datetime.strptime(str(date.today())+"T00:00:01Z","%Y-%m-%dT%H:%M:%SZ")
        today = today - timedelta(days=14)
        query = """
        select count(po.id_supplier),s.name,sum(inv.total),po.id_currency, po.id_supplier
        from purchase_order po, supplier s, invoices inv
        where inv.id_purchase_order = po.id 
        and po.id_supplier = s.id 
        and inv.paid = True
        and paid_at >= %s
        group by po.id_currency,s.name,po.id_supplier
        order by s.name desc
        limit 5
        """
        records = (today.timestamp(),)
        cursor['cursor'].execute(query,records)
        data = cursor['cursor'].fetchall()
        print(data)
        return json({'data':data,'code':200},200)
    except (Exception , psycopg2.Error)as error:
        print(error)
        return json({"error":str(error),"code":500},500)

async def top_supplier_by_INVP():
    try:
        cursor = connectPSQL
        query = """
        select count(inv.id),s.name,sum(inv.totals)
        from purchase_order po, supplier s, invoices inv
        where po.id_supplier = s.id and inv.id_purchase_order = po.id and inv.id_status = 0
        group by s.name,inv.totals
        order by s.name desc
        limit 5
        """
        cursor['cursor'].execute(query)
        data = cursor['cursor'].fetchall()
        return json({'data':data,'code':200},200)
    except (Exception , psycopg2.Error)as error:
        return json({"error":str(error),"code":500},500)


async def amount_paid_inv_by_user():
    try:
        cursor = connectPSQL()
        today = today =datetime.strptime(str(date.today())+"T00:00:01Z","%Y-%m-%dT%H:%M:%SZ")
        today = today - timedelta(days=14)
        query = """
        select sum(inv.total),count(inv.id)
        from invoices inv,users u
        where inv.id_user = %s
        """
        records = (today.timestamp(),)
        cursor['cursor'].execute(query,records)
        data = cursor['cursor'].fetchone()
        return json({'data':data,'code':200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def po_quantity_Pro_UnPro_by_week_or_month(request):
    try:
        obj = []
        cursor = connectPSQL()
        today =datetime.strptime(str(date.today())+"T23:59:59Z","%Y-%m-%dT%H:%M:%SZ")
        if request['week'] ==True:
            days = today - timedelta(days=6)
        else:
            days =  today - timedelta(month=1)
        while(days < today):
            tomorrow = days + timedelta(days=1)
            query = """
            select count(po.id)
            from purchase_order po
            where completed_at >= %s
            and completed_at <= %s 
            and completed = True
            """
            records = (days.timestamp(),tomorrow.timestamp(),)
            cursor['cursor'].execute(query,records)
            data = cursor['cursor'].fetchone()
            obj.append(data)
            days = days + timedelta(days=1)
        return json({'data':data,'code':200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def inv_quantity_Paid_by_week_or_month(request):
    try:
        obj = []
        cursor = connectPSQL()
        today =datetime.strptime(str(date.today())+"T23:59:59Z","%Y-%m-%dT%H:%M:%SZ")
        if request['week'] ==True:
            days = today - timedelta(days=6)
        else:
            days =  today - timedelta(month=30)
        while(days < today):
            tomorrow = days + timedelta(days=1)
            query = """
            select count(inv.id)
            from invoices inv
            where paid_at >= %s
            and paid_at <= %s 
            and id_status = 0
            """
            records = (days.timestamp(),tomorrow.timestamp(),)
            cursor['cursor'].execute(query,records)
            data = cursor['cursor'].fetchone()
            obj.append(data)
            week = week + timedelta(days=1)
        return json({'data':data,'code':200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def inv_quantity_Pro_by_week_or_month(request):
    try:
        obj = []
        cursor = connectPSQL()
        today =datetime.strptime(str(date.today())+"T23:59:59Z","%Y-%m-%dT%H:%M:%SZ")
        if request['week'] ==True:
            days = today - timedelta(days=6)
        else:
            days =  today - timedelta(month=1)
        while(days < today):
            tomorrow = days + timedelta(days=1)
            query = """
            select count(inv.id)
            from invoices inv
            where paid_at >= %s
            and paid_at <= %s 
            """
            records = (days.timestamp(),tomorrow.timestamp(),)
            cursor['cursor'].execute(query,records)
            data = cursor['cursor'].fetchone()
            obj.append(data)
            week = week + timedelta(days=1)
        return json({'data':data,'code':200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)