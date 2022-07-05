from sanic import Sanic
from sanic_cors import CORS
from sanic_scheduler import SanicScheduler
from api import api
from sanic.log import logger
from sanic.exceptions import ServerError
from utilities.exceptions import mongo_exception, expired_signature, no_authorization, invalid_header, invalid_token, jwt_decode_error, revoked_token, server_error_handler, wrong_token, fresh_token_required, access_denied,time_exception
from pymongo.errors import PyMongoError
from sanic_jwt_extended import JWT
from datetime import timedelta
from sanic_scheduler import SanicScheduler
from sanic.log import logger
from sanic_openapi import openapi2_blueprint
import paypalrestsdk
from paypalrestsdk.openid_connect import Tokeninfo


app = Sanic("TG")
app.blueprint(api)
app.blueprint(openapi2_blueprint)
scheduler = SanicScheduler(app)
CORS(app, automatic_options=True)

#####swagger configuration###############
app.config.API_HOST = "192.168.0.135:7600"
app.config.API_VERSION = "0.0.1"
app.config.API_TITLE = "LoreBI | Facturation System"
app.config.API_DESCRIPTION = ""

app.error_handler.add(PyMongoError, mongo_exception)
app.error_handler.add(ServerError, server_error_handler)

app.config.RESPONSE_TIMEOUT = 4000
app.config.REQUEST_TIMEOUT = 4000


paypalrestsdk.configure({
    'client_id': 'AVpLfV5K-YSdXohucZ3pEHaHuownRfmnMfraPtAzSOyDPpgX502_4W89rS7LpBUS8XQX7a4NWr9B73Kq',
    'client_secret': 'EN1l4VTesIZwSYt-tuigEJeI-f7YodEL5d4d45Z85NA9S9vRDFuM95L1GkfG9qhq62QfWG627r_YlSc0',
    'mode':'sandbox'
    })


with JWT.initialize(app) as manager:
    manager.config.access_token_expires = timedelta(hours=5)
    manager.config.refresh_token_expires = timedelta(weeks=1)
    manager.config.csrf_protect = True
    manager.config.csrf_request_methods = (
        'POST', 'PUT', 'PATCH', 'DELETE', 'GET')
    manager.config.jwt_csrf_header = 'X-CSRF-Token'
    manager.config.refresh_jwt_csrf_header = 'X-CSRF-Refresh'
    manager.config.secret_key = "AF3A7D8FAC625C9EC90A5C265BF7FC793B8E06D0B67A7D675430175B81D57EON[MlO17rwTNTOP:t"
    manager.config.jwt_header_key = "Authorization"
    manager.config.refresh_jwt_header_key = "X-Refresh"
    manager.handler.expired_signature = expired_signature
    manager.handler.no_authorization = no_authorization
    manager.handler.invalid_header = invalid_header
    manager.handler.invalid_token = invalid_token
    manager.handler.jwt_decode_error = jwt_decode_error
    manager.handler.wrong_token = wrong_token
    manager.handler.revoked_token = revoked_token
    manager.handler.fresh_token_required = fresh_token_required
    manager.handler.access_denied = access_denied

app.run(debug=False, host="0.0.0.0", port=7650, auto_reload=True,workers=1)
