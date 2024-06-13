from django.contrib import admin
from grnentry.models import Grnentry1,FormData,ProcessDetails,Delivery,Inventory,Grnentry1,fields,material,Employee_info,calibration,master_component,Outsourse


# Register your models here.



class grnentry1(admin.ModelAdmin):
    list_display=('grnentry_GRNNO','grnentry_MATERIALDESCRIPTION','grnentry_MATERIALGRADE','grnentry_QUANTITYTYPE','grnentry_NOQUANTITY','grnentry_DATETIME','grnentry_STOREOWNER','grnentry_ORDERTYPE','grnentry_CUSTOMERCODE','grnentry_PONO','grnentry_CHALLANNO','grnentry_COMMENTS','grnentry_SONO','grnentry_PARTNAME','grnentry_DRAWINGNO','REVISIONNO','grnentry_EXPTIME','FILE')    
    admin.site.register(Grnentry1)

'''
class order(admin.ModelAdmin):
    list_display=('GRNNO','quantitycheck','report','exptime','acttime','image')    

    admin.site.register(order)
    '''

class FormData(admin.ModelAdmin):
    list_display=('GRNNO','vendor_name','exptime','quantitycheck','image','report')   
    admin.site.register(FormData)   

class ProcessDetails(admin.ModelAdmin):
    list_display=('process','process','description','start_date','end_date','quantity')
    admin.site.register(ProcessDetails)

class Delivery(admin.ModelAdmin):
    list_display=('SOORDER','FINISHEDQTY','PDIREPORT','TTL_QNT_DISPATCH','INVOICENO','CUSTOMERNAME','BUYERNAME','SALESREPRESENT','PARTCOST')
    admin.site.register(Delivery)  

class Inventory(admin.ModelAdmin):
    list_display=('remaining_quantity')
    admin.site.register(Inventory)    

class fields(admin.ModelAdmin):
    list_display=('field')
    admin.site.register(fields)   

class material(admin.ModelAdmin)    :
    list_display=('part_description','DRAW_NO','Material_Grade','Finish_size','Raw_material_size','order_size','DRAWING_PDF')
    admin.site.register(material)

class Employee_info(admin.ModelAdmin):
    list_display=('name','Designation','aadhar_no','mobile_no')
    admin.site.register(Employee_info)  


class calibration(admin.ModelAdmin):
    list_display=('inst_name','make','least_count','least_count_unit','least_range','max_range','range_unit','location','calibrated_date','next_calibration_due_date','remark')
    admin.site.register(calibration) 

class master_component(admin.ModelAdmin):
    list_display=('description','drawing_no','revision_no','drawing_pdf')
    admin.site.register(master_component)


class outsourse(admin.ModelAdmin):
    list_display=('grnno','supplier_name','operation_name','part_desc','quantity','out_date','accepted_qty','rate','status')
    admin.site.register(Outsourse)    