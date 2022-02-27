from sanic_jwt_extended.decorators import jwt_required
from sanic import Blueprint
from models import purchase_order
from sanic_jwt_extended.tokens import Token
from sanic.request import Request

po = Blueprint('purchase_order', url_prefix='/purchase_order')
@po.route('/add', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return purchase_order.addPurchaseOrder(request.json,token.identity)

@po.route('/del', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return purchase_order.delpurchaseOrder(request.json)

@po.route('/search', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return purchase_order.searchpurchaseOrder(request.json)

@po.route('/update', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return purchase_order.updatePurchaseOrder(request.json)