from sanic import Blueprint
from controllers.authRoute import ar
from controllers.supplierRoute import s
from controllers.notificationsRoute import n
from controllers.rolesRoute import ro


api = Blueprint.group(ar,s,n,ro, url_prefix='/api')