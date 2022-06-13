from datetime import datetime
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json
from models.notifications import addNotification

async def payInvoice(request,data):
    try:
        cursor : connectPSQL()
        query = """
            UPDATE invoice set 
                paid = True,
            WHERE id = %s"""
        records = (request["id"],)
        cursor["cursor"].execute(query,records)
        cursor["conn"].commit()

        query="""SELECT id FROM users WHERE id=4"""
        cursor['cursor'].execute(query)
        users = cursor['cursor'].fetchall()

        query="""SELECT * FROM users WHERE id=%s"""
        cursor['cursor'].execute(query,(data,))
        user = cursor['cursor'].fetchone()


        for x in users:
            await addNotification({
                'destination':x,
                'source':data,
                'description':"Factura #{id} asignada a {user} ha sido pagada".format(id=request['id'],user=user[4]+ ' ' + user[5])
            })
        return json({"data":"Factura #{id} ha sido pagada con éxito".format(id=request['id']),'code':200},200)
    except (Exception,psycopg2.Error) as error:
        return json({'error':str(error), 'code':500},500)