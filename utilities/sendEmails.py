from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from unicodedata import name
from sanic.response import json

def sendPurchaseOrder():
    try:
        message = MIMEMultipart()

        password = "26473558cj"
        message['From'] = 'carlosp@diemo.com.ve'
        message['To'] = 'carlosp@diemo.com.ve'
        message['Subject']="LoreBi"
        message.attach(MIMEText("Orden de Compra #{id}".format(id =  1234), 'plain'))
        # create server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        
        server.starttls()
        
        # Login Credentials for sending the mail
        
        
        # send the message via the server.

        attach_file_name = 'purchase_order.pdf'
        attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
        payload = MIMEBase('application', 'octate-stream',name=attach_file_name)
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload) #encode the attachment
        #add payload header with filename
        payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
        message.attach(payload)
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        server.login(message['From'], password)
        text = message.as_string()
        server.sendmail(message['From'], message['To'],text)
        server.quit()
    except Exception as error:
         return json({"data":error,"code":500},500)

def sendPswAdm(destinatario,msgA):
    try:
        msg = MIMEMultipart()

        password = "bxbgeryvljjkccvg"
        msg['From'] = 'carlosjpa1305@gmail.com'
        msg['To'] = destinatario
        msg['Subject']='LoreBI CA'
        msg.attach(MIMEText(msgA, 'plain'))
      
        # create server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        
        server.starttls()
        
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        
        
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'],msg.as_string())

        server.quit()
    except Exception as error:
        return json({"data":str(error),"code":500},500)