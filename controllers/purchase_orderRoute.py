from sanic_jwt_extended.decorators import jwt_required
from sanic import Blueprint
from models import purchase_order
from sanic_jwt_extended.tokens import Token
from sanic.request import Request
from utilities import pdf

po = Blueprint('purchase_order', url_prefix='/purchase_order')
@po.route('/add', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    request.json["preview"]= False
    return purchase_order.addPurchaseOrder(request.json,token.identity)

@po.route('/del', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return purchase_order.delpurchaseOrder(request.json)

@po.route('/read', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return purchase_order.readPurchaseOrder(request.json)

@po.route('/update', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return purchase_order.updatePurchaseOrder(request.json,token.identity)

@po.route('/list', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return purchase_order.listPurchaseOrder()

@po.route('/productsSelect', methods=['GET'])
# @jwt_required
def ping(request: Request):
    return purchase_order.selectProducts()

@po.route('/pdfPurchaseOrder', methods=['GET'])
# @jwt_required
def ping(request: Request):

    return pdf.pdfPurchaseOrder(request.json)

@po.route('/currency', methods=['GET'])
@jwt_required
async def ping(request: Request, token:Token):
    return await purchase_order.listCurrency()

@po.route('/showPDF', methods=['POST'])
# @jwt_required
def ping(request: Request):
    
    return pdf.showPDF(request.json)

@po.route('/previewPDF', methods=['POST'])
@jwt_required
def ping(request: Request,token:Token):
    request.json["preview"]= True
    return purchase_order.addPurchaseOrder(request.json,token.identity)