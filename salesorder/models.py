from django.db import models

# Create your models here.


class salesorder(models.Model):
    salesorder_id=models.CharField(max_length=200)
    zcrm_potential_id=models.CharField(max_length=200)
    zcrm_potential_name=models.CharField(max_length=200)
    customer_name=models.CharField(max_length=200)
    customer_id=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    delivery_date=models.CharField(max_length=200)
    company_name=models.CharField(max_length=200)
    color_code=models.CharField(max_length=200)
    current_sub_status_id=models.CharField(max_length=200)
    current_sub_status=models.CharField(max_length=200)
    pickup_location_id=models.CharField(max_length=200)
    salesorder_number=models.CharField(max_length=200)
    reference_number=models.CharField(max_length=200)
    date=models.CharField(max_length=200)
    shipment_date=models.CharField(max_length=200)
    shipment_days=models.CharField(max_length=200)
    due_by_days=models.CharField(max_length=200)
    due_in_days=models.CharField(max_length=200)
    currency_id=models.CharField(max_length=200)
    source=models.CharField(max_length=200)
    currency_code=models.CharField(max_length=200)
    total=models.IntegerField()
    bcy_total=models.IntegerField()
    total_invoiced_amount=models.IntegerField()
    created_time=models.CharField(max_length=200)
    last_modified_time=models.CharField(max_length=200)
    is_emailed=models.BooleanField()
    quantity_invoiced=models.CharField(max_length=200)
    order_status=models.CharField(max_length=200)
    invoiced_status=models.CharField(max_length=200)
    paid_status=models.CharField(max_length=200)
    status=models.CharField(max_length=200)
    salesperson_name=models.CharField(max_length=200)
    branch_id=models.CharField(max_length=200)
    branch_name=models.CharField(max_length=200)
    has_attachment=models.BooleanField()
    custom_fields_list=models.CharField(max_length=200)
    delivery_method=models.CharField(max_length=200)
    delivery_method_id=models.CharField(max_length=200)
     
    def __str__(self) -> str:
        return f"{self.salesorder_id}"