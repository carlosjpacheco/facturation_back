from sanic_jwt_extended.decorators import jwt_required
from sanic import Blueprint
from models import payments
from sanic_jwt_extended.tokens import Token
from sanic.request import Request

p = Blueprint('payments', url_prefix='/payments')

@p.route('/payment', methods=['POST'])
@jwt_required
def ping(request: Request, token: Token):
    return payments.payInvoice(request.json,token.identity)

@p.route('/execute', methods=['POST'])
@jwt_required
async def ping(request: Request, token : Token):
    return await payments.sendPayment(request.json,token.identity)