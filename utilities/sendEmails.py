from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from unicodedata import name
from sanic.response import json
from email.message import EmailMessage

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

def sendPswAdm(destinatario,msgA,request):
    try:
        msg = EmailMessage()
        password = "bxbgeryvljjkccvg"
        msg['From'] = 'carlosjpa1305@gmail.com'
        msg['To'] = 'carlosjpa13@gmail.com'
        msg['Subject']='LoreBI CA'
        msg.attach(MIMEText(msgA, 'plain'))
        msg.set_content('''
        <!DOCTYPE html>
        <html>
            <body style="text-align:center;">
                <div style="padding:20px 0px;text-align:center;display:flex;">
                    <div style="height: 500px;width:400px;text-align:center;">
                        <div style="background-color:#3C49BD;padding:10px 20px;text-align:center;display:block;">
                            <h2 style="font-family:Georgia, 'Times New Roman', Times, serif;color:#F7F8FC;">Recuperación de contraseña</h2>
                        </div>
                        <img src="https://scontent-bog1-1.xx.fbcdn.net/v/t1.18169-9/13902758_1765973353659765_2515708523114629158_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=bwAUI6NqNFYAX-xvVXA&_nc_ht=scontent-bog1-1.xx&oh=00_AT8LW49TtyQO7zTW7ajn7sDhNM4pZOiyymRl4rdCdhBHMQ&oe=62E3DBD1" style="height: 300px;position:absolute;margin-top:0;display:block;margin:auto;">
                        <div style="background:#3C49BD;">
                            <h2 style="color:#F8F8FE;">Tu contraseña es</h2>
                            <h2 style="color:#F8F8FE">{psw}</h2>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        '''.format(psw = request['psw']), subtype='html')
      
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(msg['from'], password) 
            smtp.send_message(msg)
    except Exception as error:
        return json({"data":str(error),"code":500},500)

def updatePsw(destinatario,msgA,request):
    try:
        # msg = MIMEMultipart()
        msg = EmailMessage()
        password = "bxbgeryvljjkccvg"
        msg['From'] = 'carlosjpa1305@gmail.com'
        msg['To'] = 'carlosjpa13@gmail.com'
        msg['Subject']='LoreBI CA'
        msg.attach(MIMEText(msgA, 'plain'))
        msg.set_content('''
        <!DOCTYPE html>
        <html>
            <body style="text-align:center;">
                <div style="padding:20px 0px;text-align:center;display:flex;">
                    <div style="height: 500px;width:400px;text-align:center;">
                        <div style="background-color:#3C49BD;padding:10px 20px;text-align:center;display:block;">
                            <h2 style="font-family:Georgia, 'Times New Roman', Times, serif;color:#F7F8FC;">Tu contraseña ha sido actualizada</h2>
                        </div>
                        <img src="https://scontent-bog1-1.xx.fbcdn.net/v/t1.18169-9/13902758_1765973353659765_2515708523114629158_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=bwAUI6NqNFYAX-xvVXA&_nc_ht=scontent-bog1-1.xx&oh=00_AT8LW49TtyQO7zTW7ajn7sDhNM4pZOiyymRl4rdCdhBHMQ&oe=62E3DBD1" style="height: 300px;position:absolute;margin-top:0;display:block;margin:auto;">
                        <div style="background:#3C49BD;">
                            <h2 style="color:#F8F8FE;">Tu nueva contraseña es</h2>
                            <h2 style="color:#F8F8FE">{psw}</h2>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        '''.format(psw = request['psw']), subtype='html')
      
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(msg['from'], password) 
            smtp.send_message(msg)

        return json({"ok":"ok"})
    except Exception as error:
        return json({"data":str(error),"code":500},500)

def userRegistered(destinatario,msgA,request):
    try:
        msg = EmailMessage()
        password = "bxbgeryvljjkccvg"
        msg['From'] = 'carlosjpa1305@gmail.com'
        msg['To'] = 'carlosjpa13@gmail.com'
        msg['Subject']='LoreBI CA'
        msg.attach(MIMEText(msgA, 'plain'))
        msg.set_content('''
        <!DOCTYPE html>
        <html>
            <body style="text-align:center;">
                <div style="padding:20px 0px;text-align:center;display:flex;">
                    <div style="min-height: 500px;width:400px;text-align:center;height:auto;">
                        <div style="background-color:#3C49BD;padding:10px 20px;text-align:center;display:block;">
                            <h2 style="font-family:Georgia, 'Times New Roman', Times, serif;color:#F7F8FC;">Bienvenido al sistema de facturación de LoreBI</h2>
                        </div>
                        <img src="https://scontent-bog1-1.xx.fbcdn.net/v/t1.18169-9/13902758_1765973353659765_2515708523114629158_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=bwAUI6NqNFYAX-xvVXA&_nc_ht=scontent-bog1-1.xx&oh=00_AT8LW49TtyQO7zTW7ajn7sDhNM4pZOiyymRl4rdCdhBHMQ&oe=62E3DBD1" style="height: 300px;position:absolute;margin-top:0;display:block;margin:auto;">
                        <div style="background:#3C49BD;">
                            <h2 style="color:#F8F8FE;">Usuario</h2>
                            <h2 style="color:#F8F8FE">{username}</h2>
                            <h2 style="color:#F8F8FE;">Contraseña</h2>
                            <h2 style="color:#F8F8FE">{psw}</h2>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        '''.format(username = request['username'],psw = request['psw']), subtype='html')
      
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(msg['from'], password) 
            smtp.send_message(msg)

        return json({"ok":"ok"})
    except Exception as error:
        print(error)
        return json({"data":str(error),"code":500},500)