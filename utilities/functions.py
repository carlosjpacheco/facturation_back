import base64
import hashlib
from sanic.response import json 

def encodePsw(password):
    try:
        password = password.encode("UTF-8")
        encrypt = base64.b64encode(password)
        return encrypt
    except Exception as error:
        return json({"error":str(error),"code":500},500)
    
def decodePsw(password):
    try:
        print(password)
        base64_bytes = password.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        print(message)
        return message
    except Exception as error:
        print(error)
        return json({"error":str(error),"code":500},500)