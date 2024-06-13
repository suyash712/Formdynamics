from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


# Create your models here.


class Grnentry1(models.Model):
    status =[

    ]
    QUANTITY_TYPE_CHOICES = [
        ('KG', 'KG'),
        ('NO_S', 'NO\'S'),
    ]
    ORDER_TYPE_CHOICES = [
        ('WITH MATERIAL', 'With Material'),
        ('JOB WORK', 'Job Work'),
    ]
    STORE_OWNER_CHOICES = [
        ('YOGESH PALKAR','YOGESH PALKAR'),
        ('PRANAV PATIL','PRANAV PATIL'),
        ('SHUBHAM BHALERAO','SHUBHAM BHALERAO')
    ]

    MATERIAL_GRADE_CHOICES = [
        ('EN8', 'EN8'),
        ('EN9', 'EN9'),
        ('EN24', 'EN24'),
        ('EN1A', 'EN1A'),
        ('ALU T6 6082', 'ALU T6 6082'),
        ('ALU T6 5082', 'ALU T6 5082'),
        ('SS 316', 'SS 316'),
        ('SS 304', 'SS 304'),
        ('MS', 'MS'),




    ]

    grnentry_GRNNO=models.CharField(max_length=200)
    grnentry_MATERIALDESCRIPTION=models.TextField(max_length=200)
    grnentry_MATERIALGRADE = models.CharField(max_length=20, choices=MATERIAL_GRADE_CHOICES)
    grnentry_QUANTITYTYPE = models.CharField(max_length=200, choices=QUANTITY_TYPE_CHOICES)
    grnentry_NOQUANTITY = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    grnentry_DATETIME=models.DateTimeField(max_length=200,auto_now_add=True)
    grnentry_STOREOWNER=models.CharField(max_length=200, choices=STORE_OWNER_CHOICES)
    grnentry_ORDERTYPE=models.CharField(max_length=200, choices=ORDER_TYPE_CHOICES)
    grnentry_PONO=models.CharField(max_length=200)
    grnentry_CHALLANNO=models.CharField(max_length=200)
    grnentry_COMMENTS=models.TextField(max_length=200)
    grnentry_SONO=models.CharField(max_length=200)
    grnentry_PARTNAME=models.CharField(max_length=200)
    grnentry_DRAWINGNO=models.CharField(max_length=200)
    REVISIONNO=models.CharField(max_length=200)
    grnentry_EXPTIME=models.DateTimeField(max_length=200)
    status= models.CharField(max_length=50, default='Pending')
    FILE=models.FileField(upload_to='grnentryfile/')

    def __str__(self):
        return self.grnentry_GRNNO

class FormData(models.Model):
    vendor_name = models.CharField(max_length=100)
    exptime = models.DateTimeField()
    quantitycheck = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')
    report = models.TextField()
    order_status = models.CharField(max_length=50, default='Pending')
    dispatch_time = models.DateTimeField(null=True, blank=True)
    grn_entry = models.ForeignKey(Grnentry1, on_delete=models.CASCADE)

    def __str__(self):
        return self.vendor_name

    def update_order_status(self):
        # Get all process details associated with this form data
        process_details = self.processdetails_set.all()
        
        # Check if all process details are completed
        if process_details.filter(completed=False).exists():
            self.order_status = 'Pending'
        else:
            self.order_status = 'Completed'
        
        self.save()

class ProcessDetails(models.Model):
    form_data = models.ForeignKey(FormData, on_delete=models.CASCADE)
    process = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    quantity = models.IntegerField()
    completed = models.BooleanField(default=False)
    completed_time = models.DateTimeField(blank=True, null=True)
    grn_entry = models.ForeignKey(Grnentry1, on_delete=models.CASCADE)

    def mark_as_completed(self):
        self.completed_time = timezone.now()
        self.save()





class Delivery(models.Model):
    form_data = models.ForeignKey(FormData, on_delete=models.CASCADE)
    SOORDER = models.CharField(max_length=100)
    FINISHEDQTY = models.IntegerField()
    PDIREPORT = models.FileField(upload_to='pdireports/')
    TTL_QNT_DISPATCH = models.IntegerField()
    INVOICENO = models.CharField(max_length=100)
    CUSTOMERNAME = models.CharField(max_length=100)
    BUYERNAME = models.CharField(max_length=100)
    SALESREPRESENT = models.CharField(max_length=100)
    PARTCOST = models.DecimalField(max_digits=10, decimal_places=2)

   
   
class Inventory(models.Model):
    delivery =models.ForeignKey(Delivery, on_delete=models.CASCADE)
    form_data = models.ForeignKey(FormData, on_delete=models.CASCADE)
    remaining_quantity = models.IntegerField(default=0)

class fields(models.Model):
    field=models.CharField(max_length=200)



class material(models.Model):
        part_description=models.CharField(max_length=200)
        DRAW_NO=models.CharField(max_length=200)
        Material_Grade=models.CharField(max_length=200)
        Finish_size=models.CharField(max_length=200)
        Raw_material_size=models.CharField(max_length=200)
        order_size=models.CharField(max_length=200)
        DRAWING_PDF=models.FileField(upload_to='materialpdf/')



class Employee_info(models.Model):
    name=models.CharField(max_length=200)
    Designation=models.CharField(max_length=200)
    aadhar_no=models.CharField(max_length=200)
    mobile_no=models.CharField(max_length=200)

make = [
        ('mithutoyo', 'mithutoyo'),
        ('insize', 'insize'),
        ('bakers', 'bakers'),
        ('ensons', 'ensons'),
        ('aerospace', 'aerospace'),
        ('workzone', 'workzone'),
        ]

UNIT_CHOICES = [
    ('mm', 'mm'),
    ('cm', 'cm'),
    ('m', 'm'),
    ('km', 'km'),
    ('in', 'in'),
    ('ft', 'ft'),
    ('yd', 'yd'),
    ('mi', 'mi'),
]

class calibration(models.Model):
    inst_name=models.CharField(max_length=200)
    make=models.CharField(max_length=200,choices=make) 
    least_count=models.IntegerField()
    least_count_unit=models.CharField(max_length=200,choices=UNIT_CHOICES)
    least_range=models.IntegerField()
    max_range=models.IntegerField()
    range_unit=models.CharField(max_length=200,choices=UNIT_CHOICES)
    location=models.CharField(max_length=200)
    calibrated_date=models.DateTimeField()
    next_calibration_due_date=models.DateTimeField()
    remark=models.CharField(max_length=200)

class master_component(models.Model):
    description=models.CharField(max_length=200)
    drawing_no=models.CharField(max_length=200)
    revision_no=models.CharField(max_length=200)
    drawing_pdf=models.FileField(upload_to='master_drawing/')    

status=[
    ('pending','pending'),
    ('completed','completed')
]



class Outsourse(models.Model):
    grnno=models.CharField(max_length=200)
    supplier_name=models.CharField(max_length=200)
    operation_name=models.CharField(max_length=200)
    part_desc=models.CharField(max_length=200)
    quantity=models.IntegerField()
    out_date=models.DateTimeField()
    accepted_qty=models.IntegerField()
    rate=models.IntegerField()
    status=models.CharField(max_length=200,default='pending')
    completed_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.grnno



