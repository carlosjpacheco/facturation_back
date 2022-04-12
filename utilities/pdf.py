from ctypes import alignment
from datetime import date, datetime
from sanic.response import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table,Paragraph, Spacer
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY,TA_RIGHT 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from sanic.response import file
from uuid import uuid4
from utilities.sendEmails import sendPurchaseOrder
from reportlab.graphics.shapes import Drawing
 

async def pdfPurchaseOrder(request):
    try:
        
        products = {{'CPU','200 pulgadas',20},{'Monitores DELL','Estan lacras',20},{'Mouse','Con lucesitas',15},{'Teclado gamer','que tenga todas las letras',15}}
        answers = []
        answers2=[]
        answers3=[]
        Story = []
        
        answers.append(['Datos del Cliente','Datos del Proveedor'])
        answers2.append(['Nombre Completo:','The SoftWare House','Nombre:',request["name"]])
        answers2.append(['DNI:','J-5526222','DNI:','J-22629292'])
        answers2.append(['Dirección:','Casa Amarilla','Dirección:',request["address"]])
        answers3.append(['Referencia','Producto','Descripción','Unidades'])
        for x in request["products"]:
            row = [str(uuid4())[-8:],x[0],x[1],x[2]]
            answers3.append(row)


        doc = SimpleDocTemplate("purchase_order.pdf", pagesize=letter,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=18)
        estilo = getSampleStyleSheet()
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
        Story.append(Paragraph('Orden de Compra <strong># {id}</strong>'.format(id = "5582"),estiloT))
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
        Story.append(Paragraph('<strong>Dirección de entrega:</strong> {address}'.format(address = "En el kiosco"),estiloN))  
        Story.append(Spacer(1, 20))
        Story.append(Paragraph('<strong>Firma de receptor: ___________________</strong> ',estilosfirma))  
        doc.build(Story)
        sendPurchaseOrder()    
        return await file ("/home/carlos/Desktop/tg/facturation_back/purchase_order.pdf")
    except Exception as error:
        return json({"error":str(error),"code":500},500)