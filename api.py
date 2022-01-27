from sanic import Blueprint
from controllers.authRoute import ar
from controllers.supplierRoute import s
from controllers.notificationsRoute import n


api = Blueprint.group(ar,s,n, url_prefix='/api')