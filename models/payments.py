from datetime import datetime
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json
from models.notifications import addNotification
from uuid import uuid4
from paypalrestsdk import Payout, ResourceNotFound,Refund
import random

async def payInvoice(request,data):
    try:
        cursor = connectPSQL()
        date = datetime.now().timestamp()
        query = """
            UPDATE invoices set 
                id_status = 0,
                paid_at = %s
            WHERE id = %s"""
        records = (date ,request["id"],)
        cursor["cursor"].execute(query,records)

        query="""SELECT id FROM users WHERE id_role=4"""
        cursor['cursor'].execute(query)
        users = cursor['cursor'].fetchall()

        query="""SELECT * FROM users WHERE id=%s"""
        cursor['cursor'].execute(query,(data,))
        user = cursor['cursor'].fetchone()


        query="""SELECT * FROM supplier WHERE email=%s"""
        cursor['cursor'].execute(query,(request['receiver'],))
        supplier = cursor['cursor'].fetchone()
        for x in users:
            await addNotification({
                'destination':x,
                'source':data,
                'description':"Factura #{id} asignada a {user} ha sido pagada".format(id=request['id'],user=user[4]+ ' ' + user[5])
            })
        await addNotification({
                'destination':supplier[0],
                'source':data,
                'description':"Factura #{id} ha sido pagada".format(id=request['id'])
            })
        
        cursor["conn"].commit()
        return json({"data":"Factura #{id} ha sido pagada con éxito".format(id=request['id']),'code':200},200)
    except (Exception,psycopg2.Error) as error:
        print(error)
        return json({'error':str(error), 'code':500},500)

async def sendPayment(request,data):
    try:
        payout = Payout({
        "sender_batch_header": {
            "sender_batch_id": str(uuid4()),
            "email_subject": request['subject']
        },
        "items": [
            {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": request['value'],
                    "currency": "USD"
                },
                "receiver": request["receiver"],
                "note": request["subject"],
                "sender_item_id": "item_1"
            }
            ]
        })

        if payout.create(sync_mode=False):
            await payInvoice({'id':request['id'],"receiver":request['receiver']},data)
            return json({"data":'Pago creado','code':200},200)
        else:
            print(payout)
            return json({"error":'Error',"code":500},500)
    except Exception as error:
        return json({'error':str(error.response),"code":500},500)
