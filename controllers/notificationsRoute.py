from sanic_jwt_extended.decorators import jwt_required
from sanic import Blueprint
from models import notifications
from sanic_jwt_extended.tokens import Token
from sanic.request import Request

n = Blueprint('notifications', url_prefix='/notifications')

@n.route('/add', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return notifications.addNotification(request.json,token.identity)

@n.route('/update', methods=['POST'])
@jwt_required
async def ping(request: Request, token : Token):
    return await notifications.updateNotification(request.json,token.identity)

@n.route('/list', methods=['GET'])
@jwt_required
async def ping(request: Request, token : Token):
    return await notifications.listNotifications(token.identity)