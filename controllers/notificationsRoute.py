from sanic_jwt_extended.decorators import jwt_required
from sanic import Blueprint
from models import notifications
from sanic_jwt_extended.tokens import Token
from sanic.request import Request
from sanic_openapi import doc

n = Blueprint('notifications', url_prefix='/notifications')

@n.route('/add', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return notifications.addNotification(request.json,token.identity)

@n.route('/update', methods=['POST'])
@doc.summary("Marcar notificación como leida")
@jwt_required
async def ping(request: Request, token : Token):
    return await notifications.updateNotification(request.json,token.identity)

@n.route('/list', methods=['GET'])
@doc.summary("Listar notificaciones")
@jwt_required
async def ping(request: Request, token : Token):
    return await notifications.listNotifications(token.identity)

@n.route('/notifyAllUsers', methods=['POST'])
@doc.summary("Enviar notificación a todos los usuarios")
@jwt_required
async def ping(request: Request, token : Token):
    return await notifications.notifyAllUsers(request.json,token.identity)

@n.route('/notifyUser', methods=['POST'])
@doc.summary("Notificar a un usuario")
@jwt_required
async def ping(request: Request, token : Token):
    return await notifications.notifyUser(request.json,token.identity)

@n.route('/readManyNotifications', methods=['POST'])
@doc.summary("Marcar notificaciones como no leídas o como leídas")
@jwt_required
async def ping(request: Request, token : Token):
    return await notifications.readAllNotifications(request.json,token.identity)