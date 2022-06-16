from sanic import Blueprint
from controllers.authRoute import ar
from controllers.supplierRoute import s
from controllers.notificationsRoute import n
from controllers.rolesRoute import ro
from controllers.invoicesRoute import inv
from controllers.purchase_orderRoute import po
from controllers.paymentsRoute import p
from controllers.chartsRoute import ch
from controllers.dashboardRoute import da


api = Blueprint.group(ar,s,n,ro,inv,po,p,ch,da, url_prefix='/api')