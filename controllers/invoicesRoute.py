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

@inv.route('/delRobot', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.delRobotInvoice()

@inv.route('/processRobot', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.processInvoice()

@inv.route('/search', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.readInvoice(request.json)

@inv.route('/delPDFRobot', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.deleteRobotInvoicePDF(request.json)

@inv.route('/update', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.updateInvoice(request.json)

@inv.route('/updateUser', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.updateInvoiceUser(request.json,token.identity)

@inv.route('/rejectInvoice', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.rejectInvoice(request.json,token.identity)

@inv.route('/read', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.readInvoice(request.json)

@inv.route('/list', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.listInvoices(request.json,token.identity)

@inv.route('/listRobot', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.listInvoicesRobot()

@inv.route('/upload-file', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.uploadFile(request)

@inv.route('/listItems', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.selectItems()

@inv.route('/disableItem', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.disableOrenableItem(request.json)