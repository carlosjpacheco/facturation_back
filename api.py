from sanic import Blueprint
from controllers.authRoute import ar
from controllers.supplierRoute import s
from controllers.notificationsRoute import n
from controllers.rolesRoute import ro
from controllers.invoicesRoute import inv
from controllers.purchase_orderRoute import po


api = Blueprint.group(ar,s,n,ro,inv,po, url_prefix='/api')