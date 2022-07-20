from sanic_jwt_extended import tokens
from sanic_jwt_extended.decorators import jwt_required
from sanic import Blueprint
from models import auth
from sanic_jwt_extended.tokens import Token
from sanic.request import Request
from sanic_openapi import doc

ar = Blueprint('auth', url_prefix='/auth')

@ar.route('/signup', methods=['POST'])
@doc.summary("Registrar usuario")
@jwt_required
async def ping(request: Request, token : Token):
    return await auth.signup(request.json)

@ar.route('/login', methods=['POST'])
@doc.summary("Iniciar sesión")
def ping(request: Request):
    return auth.login(request.json)

@ar.route('/update', methods=['POST'])
@doc.summary("Editar usuario")
@jwt_required
async def ping(request: Request, token:Token):
    return await auth.updateUser(request.json)

@ar.route('/list', methods=['GET'])
@doc.summary("Listar usuario")
@jwt_required
async def ping(request: Request, token:Token):
    return await auth.listUsers()

@ar.route('/listUserOrder', methods=['GET'])
@doc.summary("Listar analistas para órdenes de compra")
@jwt_required
async def ping(request: Request, token:Token):
    return await auth.listUsersOrder()

@ar.route('/listUserInvoice', methods=['GET'])
@doc.summary("Listar analistas para facturas")
@jwt_required
async def ping(request: Request, token:Token):
    return await auth.listUsersInvoice()

@ar.route('/UserOrderRandom', methods=['GET'])
@doc.summary("Asignar usuario a orden de compra por carga de trabajo")
@jwt_required
async def ping(request: Request, token:Token):
    return await auth.UserRandomOrder()

@ar.route('/UserInvoiceRandom', methods=['GET'])
@doc.summary("Asignar usuario factura a por carga de trabajo")
@jwt_required
async def ping(request: Request, token:Token):
    return await auth.UserRandomInvoice()

@ar.route('/read', methods=['POST'])
@doc.summary("Consultar usuario")
@jwt_required
async def ping(request: Request, token:Token):
    return await auth.readUser(request.json)

@ar.route('/history', methods=['POST'])
@doc.summary("Ver historial de operaciones de usuario")
@jwt_required
async def ping(request: Request, token:Token):
    return await auth.listUsersHistory(request.json)

@ar.route('/delete', methods=['POST'])
@doc.summary("Deshabilitar usuario")
@jwt_required
async def ping(request: Request, token:Token):
    return await auth.deleteUser(request.json)

@ar.route('/search', methods=['POST'])
@jwt_required
async def ping(request: Request, token:Token):
    return await auth.searchUser(request.json)

@ar.route('/updatePassword', methods=['POST'])
@doc.summary("Cambiar contraseña")
@jwt_required
async def ping(request: Request, token:Token):
    return await auth.updatePassword(request.json)

@ar.route('/forgotPassword', methods=['POST'])
@doc.summary("Recuperar contraseña")
async def ping(request: Request):
    return await auth.forgotPassword(request.json)