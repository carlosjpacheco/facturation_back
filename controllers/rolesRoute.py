from sanic_jwt_extended.decorators import jwt_required
from sanic import Blueprint
from models import roles
from sanic_jwt_extended.tokens import Token
from sanic.request import Request

ro = Blueprint('roles', url_prefix='/roles')

@ro.route('/add', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return roles.addRole(request.json)

@ro.route('/permissionsToRole', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return roles.addPermissionsToRol(request.json)
