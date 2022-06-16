from datetime import datetime
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json
from models.notifications import addNotification
from uuid import uuid4

async def payInvoice(request,data):
    try:
        print(request)
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

        print('HOLAAAAAAAAAAAAAAAAAAAAAA')
        print(users)
        for x in users:
            print(x)
            await addNotification({
                'destination':x,
                'source':data,
                'description':"Factura #{id} asignada a {user} ha sido pagada".format(id=request['id'],user=user[4]+ ' ' + user[5])
            })
        cursor["conn"].commit()
        return json({"data":"Factura #{id} ha sido pagada con éxito".format(id=request['id']),'code':200},200)
    except (Exception,psycopg2.Error) as error:
        print(error)
        return json({'error':str(error), 'code':500},500)