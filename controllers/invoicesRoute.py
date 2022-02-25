from sanic_jwt_extended.decorators import jwt_required
from sanic import Blueprint
from models import invoices
from sanic_jwt_extended.tokens import Token
from sanic.request import Request

inv = Blueprint('invoices', url_prefix='/invoices')
@inv.route('/add', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.addInvoice(request.json,token.identity)

@inv.route('/del', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.delInvoice(request.json)

@inv.route('/search', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.searchInvoice(request.json)