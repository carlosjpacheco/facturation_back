from sanic_jwt_extended.decorators import jwt_required
from sanic import Blueprint
from models import dashboard
from sanic_jwt_extended.tokens import Token
from sanic.request import Request

da = Blueprint('dashboard', url_prefix='/dashboard')

########################### Summary of the day ################################################

@da.route('/amountPaidInInvoices', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return  dashboard.amount_paid_in_invoices_daily()

@da.route('/countInvoicesDaily', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return  dashboard.count_invoices_daily()

@da.route('/countPODaily', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return  dashboard.count_pro_unpro_daily()

########################### Summary last 15 days ################################################

@da.route('/amountPaidInInvoicesLastDays', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return  dashboard.amount_paid_in_invoices_lastDay()

@da.route('/countInvoicesLastDays', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return  dashboard.count_invoices_lastDays()

@da.route('/countPOLastDays', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return  dashboard.count_pro_unpro_LastDays()


@da.route('/topSupplier', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return  dashboard.top_supplier_by_TotalInv()
    
@da.route('/amountPaidInvByUser', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return  dashboard.amount_paid_inv_by_user()

########################### Modals ################################################

@da.route('/listInvoicesSummaryDaily', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return  dashboard.listInvoicesSummary(request.json)

@da.route('/listPurchaseOrdersSummary', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return  dashboard.listPurchaseOrderSummary(request.json)
