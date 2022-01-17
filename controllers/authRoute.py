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
    return await auth.updateUser(request.json,token.identity)