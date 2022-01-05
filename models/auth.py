from sanic_jwt_extended import JWT
from sanic.response import json

# async def login(data):
#     isValid = await validator.validLoginData(data)
#     if isValid is True:
#         return json(
#             {
#                 'data':{
#                     'user': user,
#                     'token': JWT.create_access_token(identity=user['client_id']),
#                     'refresh': JWT.create_refresh_token(identity=user['client_id'])                    
#                 },
#                 'type': 'auth',
#                 'code': 200
#             }
#         )
#     return json({'data': isValid, 'type': 'auth', 'code': 500}, 500)