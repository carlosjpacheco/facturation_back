from ctypes import alignment
from datetime import date, datetime
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

async def pdfPurchaseOrder(request,data):
    try:
        if os.path.exists(url_to_move+"ORD_nro_{name}_preview.pdf".format(name=data)):
            os.remove(url_to_move+"ORD_nro_{name}_preview.pdf".format(name=data))

        cursor = connectPSQL()
        query_search = """SELECT * from supplier WHERE id = %s"""
        cursor["cursor"].execute(query_search,(request["supplier"],))
        supplier = cursor["cursor"].fetchone()
        answers = []
        answers2=[]
        answers3=[]
        Story = []
        answers.append(['Datos del Cliente','Datos del Proveedor'])
        answers2.append(['Nombre Completo:','The SoftWare House','Nombre:',supplier[1]])
        answers2.append(['DNI:','J-5526222','DNI:','J-22629292'])
        answers2.append(['Dirección:','Casa Amarilla','Dirección:',supplier[3]])
        answers3.append(['Referencia','Producto','Descripción','Unidades'])
        for x in request["products"]:
            row = [str(uuid4())[-8:],x[0],x[1],x[2]]
            answers3.append(row)

        print("paso paso")
        if request["preview"]==True:
            doc = SimpleDocTemplate(url_to_move+"ORD_nro_{name}_preview.pdf".format(name=data), pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
        else:
            doc = SimpleDocTemplate("ORD_nro_{name}.pdf".format(name=request["nro_order"]), pagesize=letter,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=18)

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
        print("ESTAMOS QAUUU")
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
        Story.append(Paragraph('<strong>Dirección de entrega:</strong> {address}'.format(address = "En el kiosco"),estiloN))  
        Story.append(Spacer(1, 20))
        Story.append(Paragraph('<strong>Firma de receptor: ___________________</strong> ',estilosfirma))  
        doc.build(Story)
        # sendPurchaseOrder()  
        if request["preview"]==True:  
            shutil.move("purchase_order_preview.pdf",url_to_move)
            return await file (url_to_move+"purchase_order_preview.pdf")
        else:
            shutil.move("ORD_nro_{name}.pdf".format(name=request["nro_order"]),url_to_move)
            return await file (url_to_move+"ORD_nro_{name}.pdf".format(name=request["nro_order"]))
        
    except Exception as error:
        print(error)
        return json({"error":str(error),"code":500},500)

async def showPDF(request):
    try:
        archivo = request["file"]
        ruta= f"PDFs/{archivo}"
        return await file (ruta)

    except Exception as error:
        print(error)
        return json({"error":str(error),"code":500},500)