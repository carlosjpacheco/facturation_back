from sanic_jwt_extended import tokens
from sanic_jwt_extended.decorators import jwt_required
from sanic import Blueprint
from models import auth
from sanic_jwt_extended.tokens import Token
from sanic.request import Request

ar = Blueprint('auth', url_prefix='/auth')

@ar.route('/signup', methods=['POST'])
@jwt_required
async def ping(request: Request, token : Token):
    return await auth.signup(request.json)

@ar.route('/login', methods=['POST'])
def ping(request: Request):
    return auth.login(request.json)

@ar.route('/update', methods=['POST'])
@jwt_required
async def ping(request: Request, token:Token):
    return await auth.updateUser(request.json)

@ar.route('/list', methods=['GET'])
@jwt_required
async def ping(request: Request, token:Token):
    return await auth.listUsers()

@ar.route('/read', methods=['POST'])
@jwt_required
async def ping(request: Request, token:Token):
    return await auth.readUser(request.json)

@ar.route('/delete', methods=['POST'])
@jwt_required
async def ping(request: Request, token:Token):
    return await auth.deleteUser(request.json)

@ar.route('/search', methods=['POST'])
@jwt_required
async def ping(request: Request, token:Token):
    return await auth.searchUser(request.json)

@ar.route('/updatePassword', methods=['POST'])
@jwt_required
async def ping(request: Request, token:Token):
    return await auth.updatePassword(request.json,token.identity)