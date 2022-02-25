from sanic import Blueprint
from controllers.authRoute import ar
from controllers.supplierRoute import s
from controllers.notificationsRoute import n
from controllers.rolesRoute import ro
from controllers.invoicesRoute import inv


api = Blueprint.group(ar,s,n,ro,inv, url_prefix='/api')