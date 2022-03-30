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
from models.auth import signup,login

app = Sanic("TG")
app.blueprint(api)
scheduler = SanicScheduler(app)
CORS(app, automatic_options=True)

app.error_handler.add(PyMongoError, mongo_exception)
app.error_handler.add(ServerError, server_error_handler)

app.config.RESPONSE_TIMEOUT = 400000000000
app.config.REQUEST_TIMEOUT = 400000000000
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

app.run(debug=False, host="0.0.0.0", port=7660, auto_reload=True,workers=1)
