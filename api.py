from sanic import Blueprint
from controllers.authRoute import ar


api = Blueprint.group(ar, url_prefix='/api')