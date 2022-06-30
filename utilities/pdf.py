from ctypes import alignment
from datetime import date, datetime
from operator import le
from sanic.response import json, file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table,Paragraph, Spacer
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY,TA_RIGHT 
from reportlab.lib.styles import ParagraphStyle
from uuid import uuid4
from utilities.connections import connectPSQL
from utilities.sendEmails import sendPurchaseOrder
import shutil 
import os
url_to_move = "/home/carlos/Desktop/tg/invoicing-front/src/assets/PDFs/"
# url_to_move = "C:/Users/Usuario/Desktop/Angular 13-Tesis/material/src/assets\PDFs/"
url_reports = '/home/carlos/Desktop/tg/reports/'

async def pdfPurchaseOrder(request,data):
    try:
        cursor = connectPSQL()
        query_search = """SELECT * from supplier WHERE id = %s"""
        cursor["cursor"].execute(query_search,(request["supplier"],))
        supplier = cursor["cursor"].fetchone()
        query_search2 = """SELECT * from currency WHERE id = %s"""
        cursor["cursor"].execute(query_search2,(request["currency"],))
        currency = cursor["cursor"].fetchone()
        answers = []
        answers2=[]
        answers3=[]
        Story = []
        answers.append(['Datos del Cliente','Datos del Proveedor'])
        answers2.append(['Nombre Completo:','LoreBI CA','Nombre:',supplier[1]])
        answers2.append(['DNI:','J-5526222','DNI:','J-22629292'])
        answers2.append(['Dirección:','La California Sur, Ave Trieste , Quinta Rokamar','Dirección:',supplier[3]])
        answers3.append(['Referencia','Producto','Descripción','Unidades'])
        if os.path.exists(url_to_move+"ORD_nro_{name}_{supplier}_preview.pdf".format(name=data,supplier=supplier[0])):
            os.remove(url_to_move+"ORD_nro_{name}_{supplier}_preview.pdf".format(name=data,supplier=supplier[0]))

        if request["preview"]==True:
            products_list = []
            for val in request["products"]:
                list_val = []
                list_val.append(val["name"])
                list_val.append(val["description"])
                list_val.append(val["quantity"])
                products_list.append(list_val)
            request["products"]= products_list
            doc = SimpleDocTemplate("ORD_nro_{name}_{supplier}_preview.pdf".format(name=data,supplier=supplier[0]), pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
        else:
            doc = SimpleDocTemplate("ORD_nro_{name}.pdf".format(name=request["nro_order"]), pagesize=letter,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=18)
        for x in request["products"]:
            row = [str(uuid4())[-8:],x[0],x[1],x[2]]
            answers3.append(row)

        estilosfecha = ParagraphStyle('Justify', alignment= 2,fontSize = 12)
        estilosfirma = ParagraphStyle('Justify', alignment= 2,fontSize = 12,bottomMargin = 2 *cm)
        estiloN = ParagraphStyle('Justify',fontSize = 10,alignment=0,leftMargin = 1 * cm)
        estiloT = ParagraphStyle('Justify', alignment = 1, fontSize = 16)
        texto = '%s' % '<b>Fecha:  </b>'+str(date.today())
        Story.append(Paragraph(texto, estilosfecha))
        Story.append(Spacer(1, 12))

        table = Table(answers, colWidths=10 * cm)
        table2 = Table(answers2, colWidths=5 * cm)
        table3 = Table(answers3, colWidths=5 * cm)
        table.setStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')])
        table2.setStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')])
        table3.setStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')])

        Story.append(table)
        Story.append(table2)
        Story.append(Spacer(1, 12))
        if request["preview"]==False:
            Story.append(Paragraph('Orden de Compra <strong># {id}</strong>'.format(id = request["nro_order"]),estiloT))
            Story.append(Spacer(1, 12))
        else:
            Story.append(Paragraph('Orden de Compra <strong>#PREVIEW</strong>',estiloT))
            Story.append(Spacer(1, 12))
        Story.append(table3)

        for index, row in enumerate(answers3):
            bg_color = colors.white if index % 2 else colors.lightgrey
            ini, fin = (0, index), (len(row)-1, index)
            table3.setStyle([
                ("BOX", ini, fin, 0.1, colors.black),
                ('INNERGRID', ini, fin, 0.25, colors.black),
                ('BACKGROUND', ini, fin, bg_color)
            ])
        Story.append(Spacer(1, 15))
        Story.append(Paragraph('<strong>Fecha de entrega:</strong> {date}'.format(date = str(date.today())),estiloN))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph('<strong>Dirección de entrega:</strong> {address}'.format(address = request["delivery_address"]),estiloN))  
        Story.append(Spacer(1, 20))
        Story.append(Paragraph('<strong>Términos y condiciones: </strong>{terms_conditions}'.format(terms_conditions= request["terms_conditions"]),estiloN))
        Story.append(Spacer(1, 20))
        Story.append(Paragraph('<strong>Moneda de pago: </strong>{currency}'.format(currency= currency[1]),estiloN))

        Story.append(Spacer(1, 20))
        Story.append(Paragraph('<strong>Firma de receptor: ___________________</strong> ',estilosfirma))  
        doc.build(Story)
        sendPurchaseOrder(supplier[5],request["nro_order"])

        # sendPurchaseOrder()  
        if request["preview"]==True:  
            shutil.move("ORD_nro_{name}_{supplier}_preview.pdf".format(name=data,supplier=supplier[0]),url_to_move)
            return await showPDF("ORD_nro_{name}_{supplier}_preview.pdf".format(name=data,supplier=supplier[0]))
        else:
            shutil.move("ORD_nro_{name}.pdf".format(name=request["nro_order"]),url_to_move)
            return await showPDF("ORD_nro_{name}.pdf".format(name=request["nro_order"]))
        
    except Exception as error:
        return json({"error":error,"code":500},500)

async def showPDF(request):
    try:
        archivo = request
        return json({"data":archivo,"code":200},200)

    except Exception as error:
        return json({"error":str(error),"code":500},500)


async def pdfReport(request):
    try:
        answers3=[]
        Story = [] 
        id = str(uuid4())[:5]
        if 'nro_invoice' in request['list'][0]:
            answers3.append(['Ref','Total','Encargado','Proveedor','Estado','Fecha',])
            for x in request["list"]:
                user = x['user'].split(' ')
                if len(user) > 2:
                    user = user[0]+ ' '+ user[2]
                else:
                    user = user[0]+ ' '+ user[1]
                row = [x['nro_invoice'],x['total'],x['user'],x['supplier'],x['status'],str(datetime.fromtimestamp(x['date']))[:10]]
                answers3.append(row)
        else:
            answers3.append(['Ref','Encargado','Proveedor','Moneda','Estado','Fecha',])
            for x in request["list"]:
                if x['completed'] == True:
                    x['completed'] = 'Procesada'
                else:
                    x['completed'] = 'Por procesar'
                user = x['user'].split(' ')
                if len(user) > 2:
                    user = user[0]+ ' '+ user[2]
                else:
                    user = user[0]+ ' '+ user[1]

                row = [x['nro_order'],user,x['supplier'],x['currency'][0],x['completed'],str(datetime.fromtimestamp(x['date']))[:10]]
                answers3.append(row)

        doc = SimpleDocTemplate("report_{id}.pdf".format(id=id), pagesize=letter,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=18)


        estilosfecha = ParagraphStyle('Justify', alignment= 2,fontSize = 12)
        estilosfirma = ParagraphStyle('Justify', alignment= 2,fontSize = 12,bottomMargin = 2 *cm)
        estiloN = ParagraphStyle('Justify',fontSize = 10,alignment=0,leftMargin = 1 * cm)
        estiloT = ParagraphStyle('Justify', alignment = 1, fontSize = 16)
        texto = '%s' % '<b>Fecha:  </b>'+str(date.today())
        Story.append(Paragraph(texto, estilosfecha))
        Story.append(Spacer(1, 12))

        table3 = Table(answers3, colWidths=3 * cm)
        table3.setStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')])
        Story.append(Spacer(1, 12))
        if 'nro_invoice' in request['list'][0]:
            Story.append(Paragraph('<strong>Reporte de Facturas</strong>',estiloT))
        else:
            Story.append(Paragraph('<strong>Reporte de Ordenes de compras</strong>',estiloT))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph('Fecha de inicio:<strong>{start_date}</strong>'.format(start_date = str(request['start_date'])[:10]),estiloN))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph('Fecha final:<strong>{end_date}</strong>'.format(end_date = str(request['end_date'])[:10]),estiloN))
        Story.append(Spacer(1, 12))
        Story.append(table3)

        for index, row in enumerate(answers3):
            bg_color = colors.white if index % 2 else colors.lightgrey
            ini, fin = (0, index), (len(row)-1, index)
            table3.setStyle([
                ("BOX", ini, fin, 0.1, colors.black),
                ('INNERGRID', ini, fin, 0.25, colors.black),
                ('BACKGROUND', ini, fin, bg_color)
            ])

        Story.append(Spacer(1, 20))
        doc.build(Story)
        # sendPurchaseOrder()  
        shutil.move("report_{id}.pdf".format(id = id),url_reports)
        return json({'data':'El reporte ha sido creado, revise la ruta {url}report_{id}.pdf'.format(url = url_reports,id = id),'code':200},200)

        
    except Exception as error:
        return json({"error":error,"code":500},500)