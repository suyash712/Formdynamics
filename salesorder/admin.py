from django.contrib import admin
from salesorder.models import salesorder

# Register your models here.
class salesorder(admin.ModelAdmin):
    list_display=('salesorder_id','zcrm_potential_id','zcrm_potential_name','customer_name','customer_id','email','delivery_date','company_name','color_code','current_sub_status_id','current_sub_status','pickup_location_id','salesorder_number','reference_number','date','shipment_date','shipment_days','due_by_days','due_in_days','currency_id','source','currency_code','total','bcy_total','total_invoiced_amount','created_time','last_modified_time','is_emailed','quantity_invoiced','order_status','invoiced_status','paid_status','status','salesperson_name','branch_id','branch_name','has_attachment','custom_fields_list','delivery_method',' delivery_method_id')
    admin.site.register(salesorder)