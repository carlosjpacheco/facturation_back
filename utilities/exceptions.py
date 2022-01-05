from sanic_jwt_extended.exceptions import *
from pymongo.errors import PyMongoError, OperationFailure
from sanic.log import logger
from sanic import request
from sanic import response
from sanic.exceptions import ServerError,RequestTimeout

async def server_error_handler(request, exception):
    logger.error(request, exception)
    return response.json({'message': 'Ocurrió un error inesperado en el servidor.', 'type':'server_error', 'code': 500}, 500)


async def expired_signature(request: request.Request, exception: JWTExtendedException):
    message = "Expired Signature"
    code = 211
    return response.json({'message': message, 'type': 'jwt_error', 'code': code}, headers={'access-control-allow-origin': '*'}, status=500)


async def no_authorization(request: request.Request, exception: JWTExtendedException):
    message = "No authorization header"
    code = 201
    return response.json({'message': message, 'type': 'jwt_error', 'code': code}, headers={'access-control-allow-origin': '*'}, status=500)


async def invalid_header(request: request.Request, exception: JWTExtendedException):
    message = "Invalid authorization header"
    code = 202
    return response.json({'message': message, 'type': 'jwt_error', 'code': code}, headers={'access-control-allow-origin': '*'}, status=500)


async def invalid_token(request: request.Request, exception: JWTExtendedException):
    message = "Invalid authorization token"
    code = 203
    return response.json({'message': message, 'type': 'jwt_error', 'code': code}, headers={'access-control-allow-origin': '*'}, status=500)


async def jwt_decode_error(request: request.Request, exception: JWTExtendedException):
    message = "JWT Decoding error"
    code = 204
    return response.json({'message': message, 'type': 'jwt_error', 'code': code}, headers={'access-control-allow-origin': '*'}, status=500)


async def wrong_token(request: request.Request, exception: JWTExtendedException):
    message = "Wrong authorization token"
    code = 205
    return response.json({'message': message, 'type': 'jwt_error', 'code': code}, headers={'access-control-allow-origin': '*'}, status=500)


async def revoked_token(request: request.Request, exception: JWTExtendedException):
    message = "Revoked token"
    code = 206
    return response.json({'message': message, 'type': 'jwt_error', 'code': code}, headers={'access-control-allow-origin': '*'}, status=500)


async def fresh_token_required(request: request.Request, exception: JWTExtendedException):
    message = "Fresh token is required"
    code = 207
    return response.json({'message': message, 'type': 'jwt_error', 'code': code}, headers={'access-control-allow-origin': '*'}, status=500)


async def access_denied(request: request.Request, exception: JWTExtendedException):
    message = "Access denied"
    code = 208
    return response.json({'message': message, 'type': 'jwt_error', 'code': code}, headers={'access-control-allow-origin': '*'}, status=500)


async def mongo_exception(request, exception):
    logger.error(exception)
    return response.json({'message': 'Ha ocurrido un error con la comunicación a la base de datos', 'type': 'database_error', 'code': 500}, headers={'access-control-allow-origin': '*'}, status=500)

async def time_exception(request, exception : RequestTimeout):
    logger.error(exception)
    return response.json({'message': 'Ha ocurrido un error con la comunicación', 'type': 'database_error', 'code': 500}, headers={'access-control-allow-origin': '*'}, status=503)
