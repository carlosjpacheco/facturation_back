from sanic_jwt_extended.decorators import jwt_required
from sanic import Blueprint
from models import purchase_order
from sanic_jwt_extended.tokens import Token
from sanic.request import Request
from utilities import pdf
from sanic_openapi import doc

po = Blueprint('purchase_order', url_prefix='/purchase_order')

@po.route('/add', methods=['POST'])
@doc.summary("Agregar orden de compra")
@jwt_required
def ping(request: Request, token : Token):
    request.json["preview"]= False
    return purchase_order.addPurchaseOrder(request.json,token.identity)

@po.route('/del', methods=['POST'])
@doc.summary("Borrar orden de compra")
@jwt_required
def ping(request: Request, token : Token):
    return purchase_order.delpurchaseOrder(request.json)

@po.route('/read', methods=['POST'])
@doc.summary("Consultar orden de compra")
@jwt_required
def ping(request: Request, token : Token):
    return purchase_order.readPurchaseOrder(request.json)

@po.route('/update', methods=['POST'])
@doc.summary("Editar orden de compra")
@jwt_required
def ping(request: Request, token : Token):
    return purchase_order.updatePurchaseOrder(request.json,token.identity)

@po.route('/list', methods=['POST'])
@doc.summary("Listar órdenes de compra")
@jwt_required
def ping(request: Request, token : Token):
    return purchase_order.listPurchaseOrder(request.json,token.identity)

@po.route('/productsSelect', methods=['GET'])
@doc.summary("Select de productos")
@jwt_required
def ping(request: Request):
    return purchase_order.selectProducts()

@po.route('/pdfPurchaseOrder', methods=['GET'])
@doc.summary("Generar pdf de orden de compra")
@jwt_required
def ping(request: Request):
    return pdf.pdfPurchaseOrder(request.json)

@po.route('/currency', methods=['GET'])
@doc.summary("Select tipos de moneda")
@jwt_required
async def ping(request: Request, token:Token):
    return await purchase_order.listCurrency()

@po.route('/showPDF', methods=['POST'])
@doc.summary("Mostrar PDF")
@jwt_required
def ping(request: Request):
    return pdf.showPDF(request.json)

@po.route('/previewPDF', methods=['POST'])
@doc.summary("Ver preview de PDF")
@jwt_required
def ping(request: Request,token:Token):
    request.json["preview"]= True
    return purchase_order.addPurchaseOrder(request.json,token.identity)

@po.route('/report', methods=['POST'])
@doc.summary("Reporte PDF")
@jwt_required
def ping(request: Request):
    return pdf.pdfReport(request.json)