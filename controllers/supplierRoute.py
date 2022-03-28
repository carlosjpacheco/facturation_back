from sanic_jwt_extended import tokens
from sanic_jwt_extended.decorators import jwt_required
from sanic import Blueprint
from models import supplier
from sanic_jwt_extended.tokens import Token
from sanic.request import Request

s = Blueprint('supplier', url_prefix='/supplier')

@s.route('/add', methods=['POST'])
@jwt_required
async def ping(request: Request, token : Token):
    return await supplier.addSupplier(request.json)

@s.route('/delete', methods=['POST'])
@jwt_required
async def ping(request: Request, token : Token):
    return supplier.deleteSupplier(request.json)

@s.route('/update', methods=['POST'])
@jwt_required
async def ping(request: Request, token : Token):
    return await supplier.updateSupplier(request.json)

@s.route('/search', methods=['POST'])
@jwt_required
async def ping(request: Request, token : Token):
    return supplier.searchSupplier(request.json)

@s.route('/list', methods=['GET'])
@jwt_required
async def ping(request: Request, token : Token):
    return supplier.listSuppliers()

@s.route('/read', methods=['POST'])
@jwt_required
async def ping(request: Request, token:Token):
    return supplier.readSupplier(request.json)