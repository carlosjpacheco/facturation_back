from calendar import month
from datetime import date, datetime, timedelta
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json
from dateutil.relativedelta import relativedelta

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
        if len(data)==0:
            data = [[0,0,0],[0,0,0]]
        if len(data)==1 and data[0][0]==1:
            data.insert(0,[0,0,0])
        if len(data)==1 and data[0][0]==2:
            data.append([0,0,0])
        return json({'data':data,'code':200},200)
    except (Exception, psycopg2.Error) as error:
        print(error)
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
        if len(data)==0:
            data = [[0,0],[0,0]]
        if len(data)==1 and data[0][1]==False:
            data.insert(0,[0,0])
        if len(data)==1 and data[0][1]==True:
            data.append([0,[0,0]])
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
        if len(data)==0:
            data = [[0,0,0],[0,0,0]]
        if len(data)==1 and data[0][0]==1:
            data.insert(0,[0,0,0])
        if len(data)==1 and data[0][0]==2:
            data.append([0,0,0])
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
        if len(data)==1 and data[0][1]==False:
            data.insert(0,[0,0])
        if len(data)==1 and data[0][1]==True:
            data.append([0,[0,0]])
        return json({'data':data,'code':200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def top_supplier_by_TotalInv():
    try:
        cursor = connectPSQL()
        today = today =datetime.strptime(str(date.today())+"T00:00:01Z","%Y-%m-%dT%H:%M:%SZ")
        today = today - timedelta(days=14)
        query = """
        select count(po.id_supplier),s.name,sum(inv.total), cu.name
        from purchase_order po, supplier s, invoices inv, currency cu
        where inv.id_purchase_order = po.id and cu.id = po.id_currency
        and po.id_supplier = s.id 
        and inv.paid = True
        and paid_at >= %s
        group by po.id_currency,s.name,po.id_supplier, cu.name
        limit 5
        """
        records = (today.timestamp(),)
        cursor['cursor'].execute(query,records)
        data = cursor['cursor'].fetchall()
        return json({'data':data,'code':200},200)
    except (Exception , psycopg2.Error)as error:
        print(error)
        return json({"error":str(error),"code":500},500)

async def amount_paid_inv_by_user():
    try:
        cursor = connectPSQL()
        today = today =datetime.strptime(str(date.today())+"T00:00:01Z","%Y-%m-%dT%H:%M:%SZ")
        today = today - timedelta(days=14)
        query = """
        select sum(inv.total),count(inv.id), u.first_name, u.last_name, cu.name
        from invoices inv,users u, purchase_order po, currency cu
        where inv.id_user = u.id and inv.id_purchase_order = po.id and cu.id = po.id_currency
        and inv.paid_at >= %s
        group by po.id_currency,u.id, cu.name
        """
        records = (today.timestamp(),)
        cursor['cursor'].execute(query,records)
        data = cursor['cursor'].fetchall()
        return json({'data':data,'code':200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

########################### Modals ################################################

async def listInvoicesSummary(request):
    try:
        cursor = connectPSQL()
        today = today =datetime.strptime(str(date.today())+"T00:00:01Z","%Y-%m-%dT%H:%M:%SZ")
        if request['daily']==False:
            today = today - timedelta(days=14)
        invoicesArr = []
        details = []
        query_search = """
            SELECT inv.id,inv.nro_invoice,inv.id_user,inv.id_status,inv.id_purchase_order, inv.paid, inv.created_at, inv.deleted,inv.date,inv.name_supplier,inv.paid_at,inv.total, inv.paid_at
            from invoices inv , purchase_order po
            where inv.paid_at >= %s
            and inv.id_purchase_order = po.id
            group by po.id_currency,inv.id"""

        cursor["cursor"].execute(query_search,(today.timestamp(),))
        invoices = cursor["cursor"].fetchall()
        if invoices:
            for x in invoices:
                query_search = """SELECT * from purchase_order WHERE id = %s"""
                cursor["cursor"].execute(query_search,(x[4],))
                po = cursor["cursor"].fetchone()
                query_search = """SELECT name from currency WHERE id = %s"""
                cursor["cursor"].execute(query_search,(po[7],))
                currency = cursor["cursor"].fetchone()
                query_search = """SELECT * from invoices_status WHERE id = %s"""
                cursor["cursor"].execute(query_search,(x[3],))
                status = cursor["cursor"].fetchone()
                query_search = """SELECT * from invoice_detail WHERE id_invoice = %s"""
                cursor["cursor"].execute(query_search,(x[0],))
                detail = cursor["cursor"].fetchall()
                if x[2] != None:
                    query_search3 = """SELECT * from users where id = %s"""
                    cursor["cursor"].execute(query_search3,(x[2],))
                    user = cursor["cursor"].fetchone()
                    uservalue = user[4]+ " "+user[5]
                else:
                    uservalue = "Sin Asignar"
                for y in detail:
                    details.append({'amount':y[1],'product':y[2],'quantity':y[3]})
                invoicesJson = {
                    "id": x[0],
                    "nro_invoice":x[1].strip(),
                    "total":x[11],
                    "user": uservalue,
                    "supplier": x[9],
                    "status":status[1],
                    "date":x[12],
                    "products":details,
                    "currency":currency[0]
                }
                invoicesArr.append(invoicesJson)
            return json({"data":invoicesArr,"code":200},200)
        else:
            return json({"data":"No se consiguio ninguna factura","code":200},200)
    except (Exception, psycopg2.Error) as error:
        return json({"error":str(error),"code":500},500)

async def listPurchaseOrderSummary(request):
    try:
        print(request)
        cursor = connectPSQL()
        today = today =datetime.strptime(str(date.today())+"T00:00:01Z","%Y-%m-%dT%H:%M:%SZ")
        if request['daily']==False:
            today = today - timedelta(days=14)
        purchaseOrdersArr = []
        query_search = """
            select *
            from purchase_order po
            where completed_at >= %s or date >= %s
        """
        records = (today.timestamp(),today.timestamp(),)
        cursor['cursor'].execute(query_search,records)
        purchaseOrders = cursor["cursor"].fetchall()
        print("AQUIIIIIIIIII")
        if purchaseOrders:
            for x in purchaseOrders:
                query_search = """SELECT name from currency WHERE id = %s"""
                cursor["cursor"].execute(query_search,(x[7],))
                currency = cursor["cursor"].fetchone()
                query_search = """SELECT * from detail_purchase_order where id_purchase_order = %s"""
                cursor["cursor"].execute(query_search,(x[0],))
                query_search2 = """SELECT * from supplier where id = %s"""
                cursor["cursor"].execute(query_search2,(x[4],))
                supplier = cursor["cursor"].fetchone()
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
                    "currency": currency
                } 
                purchaseOrdersArr.append(purchaseOrdersJson)
            return json({"data":purchaseOrdersArr,"code":200},200)
        else:
            return json({"data":"No se consiguio ninguna orden de compra","code":200},200)
    except (Exception, psycopg2.Error) as error:
        print(error)
        return json({"error":error,"code":500},500)


########################### Chart ################################################

async def yearlyChart():
    try:
        cursor = connectPSQL()
        today = today =datetime.strptime(str(date.today())+"T00:00:01Z","%Y-%m-%dT%H:%M:%SZ")
        labelsX = []
        invoices = []
        po = []
        invPaidDo = []
        invPaidBs = []
        initYear = today - relativedelta(months=today.month-1,days=today.day-1)
        while (initYear.month <= today.month):
            datetime_object = datetime.strptime(str(initYear.month), "%m")
            full_month_name = datetime_object.strftime("%B")
            labelsX.append(full_month_name)

            queryInvoices = """
            Select count(inv.id)
            From invoices inv 
            Where paid_at >= %s
            and paid_at <= %s
            """
            records = (initYear.timestamp(),(initYear+relativedelta(months=1)).timestamp(),)
            cursor['cursor'].execute(queryInvoices,records)
            countInvoices = cursor['cursor'].fetchone()
            invoices.append(countInvoices[0])

            queryPO = """
            Select count(po.id)
            From purchase_order po 
            Where completed_at >= %s
            and completed_at <= %s
            """
            records = (initYear.timestamp(),(initYear+relativedelta(months=1)).timestamp(),)
            cursor['cursor'].execute(queryPO,records)
            countPO = cursor['cursor'].fetchone()
            po.append(countPO[0])

            queryInvPaidDo = """
            Select SUM(inv.total)
            From invoices inv, purchase_order po
            Where paid_at >= %s
            and paid_at <= %s
            and inv.id_purchase_order = po.id
            and po.id_currency = 1
            and paid = True
            """
            records = (initYear.timestamp(),(initYear+relativedelta(months=1)).timestamp(),)
            cursor['cursor'].execute(queryInvPaidDo,records)
            invDo = cursor['cursor'].fetchone()
            print(invDo[0])
            if invDo[0] is None:
                equis=0
                invPaidDo.append(equis)
            else:
                invPaidDo.append(invDo[0])

            queryInvPaidBs = """
            Select SUM(inv.total)
            From invoices inv, purchase_order po
            Where paid_at >= %s
            and paid_at <= %s
            and inv.id_purchase_order = po.id
            and po.id_currency = 2
            and paid = True
            """
            records = (initYear.timestamp(),(initYear+relativedelta(months=1)).timestamp(),)
            cursor['cursor'].execute(queryInvPaidBs,records)
            invBs = cursor['cursor'].fetchone()
            if invBs[0] is None:
                equis=0
                invPaidBs.append(equis)
            else:
                invPaidBs.append(invBs[0])

            initYear = initYear + relativedelta(months=1)

        return json({'data':{'labels':labelsX, 'invoices':invoices, 'po':po,'invPaidDo':invPaidDo,'invPaidBs':invPaidBs} ,'code': 200},200)
    except (Exception, psycopg2.Error)as error:
        return json({'error':str(error),"code":500},500)