from sanic import Blueprint
from controllers.authRoute import ar
from controllers.supplierRoute import s


api = Blueprint.group(ar,s, url_prefix='/api')