from sanic_jwt_extended.decorators import jwt_required
from sanic import Blueprint
from utilities import charts
from sanic_jwt_extended.tokens import Token
from sanic.request import Request

ch = Blueprint('charts', url_prefix='/charts')

@ch.route('/barAssign', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return charts.assign_user_purchaseOrder_bar()

@ch.route('/pieAssign', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return charts.assign_user_purchaseOrder_pie()

@ch.route('/barInvoice', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return charts.pay_invoice_bar()

@ch.route('/pieInvoice', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return charts.pay_invoice_pie()

@ch.route('/poLine', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return charts.assign_user_purchaseOrder_line()

@ch.route('/invoicesLine', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return charts.assign_user_invoices_line()