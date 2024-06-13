from django.contrib import admin
from purchaseorders.models import apipurchaseorder
# Register your models here.
class apipurchaseorder(admin.ModelAdmin):
    list_display=(
    'purchaseorder_id',
    'vendor_id',
    'vendor_name',
    'company_name',
    'order_status',
    'billed_status',
    'status',
    'color_code',
    'current_sub_status_id',
    'current_sub_status',
    'purchaseorder_number',
    'reference_number',
    'date',
    'delivery_date',
    'delivery_days',
    'due_by_days',
    'due_in_days',
    'currency_id',
    'currency_code',
    'price_precision',
    'total',
    'has_attachment',
    'created_time',
    'last_modified_time',
    'quantity_yet_to_receive',
    'quantity_marked_as_received',
    'receives',
    'client_viewed_time',
    'is_viewed_by_client',
    'branch_id',
    'branch_name',
    )

    admin.site.register(apipurchaseorder)