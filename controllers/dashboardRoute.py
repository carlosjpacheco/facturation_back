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
    
########################### Summary last 15 days ################################################

@da.route('/topSupplierByINVP', methods=['GET'])
@jwt_required
def ping(request: Request, token : Token):
    return  dashboard.top_supplier_by_INVP()

@da.route('/amountPaidInvByUser', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return  dashboard.amount_paid_inv_by_user(request.json)

@da.route('/poQuantityByWeekOrMonth', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return  dashboard.po_quantity_Pro_UnPro_by_week_or_month(request.json)

@da.route('/invQuantityPaidByWeekOrMonth', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return  dashboard.inv_quantity_Paid_by_week_or_month(request.json)

@da.route('/invQuantityProByWeekOrMonth', methods=['POST'])
@jwt_required
def ping(request: Request, token : Token):
    return  dashboard.inv_quantity_Pro_by_week_or_month(request.json)