import paypalrestsdk
from datetime import datetime
import re
import time
from utilities.connections import connectPSQL
import psycopg2
from sanic.response import json

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "CLIENT_ID",
  "client_secret": "CLIENT_SECRET" })

async def payment():

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:7650/payment/execute",
            "cancel_url": "http://localhost:7650/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "sku": "12345",
                    "price": "500.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "500.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return json({'paymentID' : payment.id})

async def execute(request):
    success = False

    payment = paypalrestsdk.Payment.find(request['paymentID'])

    if payment.execute({'payer_id' : request['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return json({'success' : success})