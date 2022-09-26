from sanic_jwt_extended.decorators import jwt_required
from sanic import Blueprint
from models import invoices
from sanic_jwt_extended.tokens import Token
from sanic.request import Request
from sanic_openapi import doc


inv = Blueprint('invoices', url_prefix='/invoices')

@inv.route('/add', methods=['POST'])
@doc.summary("Agregar factura")
@jwt_required
def ping(request: Request, token : Token):
    return invoices.addInvoice(request.json,token.identity)

@inv.route('/del', methods=['POST'])
@doc.summary("Borrar factura")
@jwt_required
def ping(request: Request, token : Token):
    return invoices.delInvoice(request.json)

@inv.route('/delRobot', methods=['GET'])
@doc.summary("Borrar factura robot")
@jwt_required
def ping(request: Request, token : Token):
    return invoices.delRobotInvoice()

@inv.route('/processRobot', methods=['GET'])
@doc.summary("Ejecutar bot")
@jwt_required
def ping(request: Request, token : Token):
    return invoices.processInvoice()

@inv.route('/search', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.readInvoice(request.json)

@inv.route('/delPDFRobot', methods=['POST'])
@doc.summary("Borrar PDF robot")
@jwt_required
def ping(request: Request, token : Token):
    return invoices.deleteRobotInvoicePDF(request.json)

@inv.route('/update', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.updateInvoice(request.json)

@inv.route('/updateUser', methods=['POST'])
@doc.summary("Asignar usuario a la factura")
@jwt_required
def ping(request: Request, token : Token):
    return invoices.updateInvoiceUser(request.json,token.identity)

@inv.route('/rejectInvoice', methods=['POST'])
@doc.summary("Rechazar factura")
@jwt_required
def ping(request: Request, token : Token):
    return invoices.rejectInvoice(request.json,token.identity)

@inv.route('/read', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.readInvoice(request.json)

@inv.route('/list', methods=['POST'])
@doc.summary("Listar facturas")
@jwt_required
def ping(request: Request, token : Token):
    return invoices.listInvoices(request.json,token.identity)

@inv.route('/listRobot', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return invoices.listInvoicesRobot()

@inv.route('/upload-file', methods=['POST'])
@doc.summary("Cargar archivo factura")
@jwt_required
def ping(request: Request, token : Token):
    return invoices.uploadFile(request)

@inv.route('/listItems', methods=['GET'])
@doc.summary("Listar items para plantillas de factura")
@jwt_required
def ping(request: Request, token : Token):
    return invoices.selectItems()

@inv.route('/disableItem', methods=['POST'])
@doc.summary("Deshabilitar items de plantilla de facturas")
@jwt_required
def ping(request: Request, token : Token):
    return invoices.disableOrenableItem(request.json)