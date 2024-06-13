from django.shortcuts import render,redirect, get_object_or_404 
from django.http import HttpResponse
from grnentry.models import Grnentry1,FormData, ProcessDetails,Delivery,Inventory,fields,material,Employee_info,calibration,master_component,Outsourse
import requests
from django.http import JsonResponse
from .forms import FormDataForm
import json
import http.client
from salesorder.models import salesorder
from apiitems.models import apiitems
from purchaseorders.models import apipurchaseorder
from django.utils import timezone
from .forms import DeliveryForm
from django.db.models import F, Sum
from django.conf import settings
import os



#render template
def index(request):
   return render(request, 'index.html')
def grnentry(request):  
   return render(request,'grnentry.html')
def home(request):
    return render(request,'home.html')      
def purchaseinfoshow(request):
    return render(request,'purchaseentryshow.html')
def maintracking(request):
    return render(request,'trackingmainpage.html')   
def trackingentry(request):
    return render(request,'trackingentry.html')
def salesorder1(request):
    return render(request,'salesorder.html')   
def purchaseorder1(request):
    return render(request,'purchaseorder1.html')
def trackentry(request):
    return render(request,'trackingentry.html') 
def inventory(request):
    return render(request,'inventory.html') 
def trackmainpage(request):
    return render(request,'trackingmainpage.html')

def materialinfo(request):
    return render(request,'materialinfo.html')

def materialinfoform(request):
    return render(request,'materialinfoform.html')

def outsourse(request):
    return render(request,'outsourse.html')



def outsourseform(request):
    if request.method == 'POST':  # Correct method check
        grnno = request.POST.get('grnno')
        supplier_name = request.POST.get('supplier_name')
        operation_name = request.POST.get('operation_name')
        part_desc = request.POST.get('part_desc')  # Correct handling
        quantity = request.POST.get('quantity') 
        out_date = request.POST.get('out_date')
        accepted_qty = request.POST.get('accepted_qty')  # Correct handling
        rate = request.POST.get('rate')
        
        en = Outsourse(grnno=grnno, supplier_name=supplier_name, operation_name=operation_name,
                       part_desc=part_desc, quantity=quantity, out_date=out_date,
                       accepted_qty=accepted_qty, rate=rate)
        en.save()

        return redirect('showoutsourse')  # Ensure this name matches your URL pattern name
    return redirect('showoutsourse')

def showoutsourse(request):
    out = Outsourse.objects.all()  # Use the correct class name
    for obj in out:
        print(obj.grnno)
    return render(request, 'outsourse.html', {'outsourse': out})

def form_view1(request, entry_id):
    grn_entry = get_object_or_404(Grnentry1, id=entry_id)

    if request.method == 'POST':
        vendor_name = request.POST.get('vendor_name')
        exptime = request.POST.get('exptime')
        quantitycheck = request.POST.get('quantitycheck')
        image = request.FILES.get('image')
        report = request.POST.get('report')

        form_data = FormData.objects.create(
            grn_entry=grn_entry,
            vendor_name=vendor_name,
            exptime=exptime,
            quantitycheck=quantitycheck,
            image=image,
            report=report
        )

        input_fields = request.POST.getlist('inputField[]')

        # Split input fields into respective categories
        process_details = input_fields[0::5]
        descriptions = input_fields[1::5]
        start_dates = input_fields[2::5]
        end_dates = input_fields[3::5]
        quantities = input_fields[4::5]

        for i in range(len(process_details)):
            ProcessDetails.objects.create(
                form_data=form_data,
                grn_entry=grn_entry,
                process=process_details[i],
                description=descriptions[i],
                start_date=start_dates[i],
                end_date=end_dates[i],
                quantity=quantities[i]
            )

        grn_entry.status = 'Completed'
        grn_entry.save()

        return redirect('display_form_data')

    return render(request, 'your_template.html', {'grn_entry': grn_entry})

def dispatch_details(request, entry_id):
    if request.method == 'POST':
        form = DeliveryForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.form_data = FormData.objects.get(id=entry_id)
            form_data.dispatch_time = timezone.now()
            form_data.save()
            
            # Update the status of the associated entry based on form completion
            entry = FormData.objects.get(id=entry_id)
            if entry.order_status == 'Completed':
                entry.order_status = 'Delivered'
            else:
                entry.order_status = 'Completed'
            entry.save()
            
            return render(request,'delivery_success.html')  # Redirect to a success page
    else:
        form = DeliveryForm()
        
    
    return render(request, 'delivery_form.html', {'form': form})

def delivery_success(request):
    return render(request, 'delivery_success.html')

#production tracking
def form_view(request):
    if request.method == 'POST':
        grnno = request.POST.get('GRNNO')
        vendor_name = request.POST.get('vendor_name')
        exptime = request.POST.get('exptime')
        quantitycheck = request.POST.get('quantitycheck')
        image = request.FILES.get('image')
        report = request.POST.get('report')

        # Save form data to the database
        form_data = FormData.objects.create(
            GRNNO=grnno,
            vendor_name=vendor_name,
            exptime=exptime,
            quantitycheck=quantitycheck,
            image=image,
            report=report
        )

        # Save process details
        process_details = request.POST.getlist('inputField[]')
        for i in range(0, len(process_details), 5):
            process = process_details[i]
            description = process_details[i+1]
            start_date = process_details[i+2]
            end_date = process_details[i+3]
            quantity = process_details[i+4]

            ProcessDetails.objects.create(
                form_data=form_data,
                process=process,
                description=description,
                start_date=start_date,
                end_date=end_date,
                quantity=quantity
            )

        # Assuming you have a separate page to display the data
        return redirect('display_form_data')

    return render(request, 'form.html')

def display_entry_details(request, entry_id):
    entry = get_object_or_404(FormData, pk=entry_id)
    process_details = entry.processdetails_set.all()
    last_completed = None
    upcoming_process_details = []
    
    # Calculate the total number of processes and completed processes
    total_processes = process_details.count()
    completed_processes = process_details.filter(completed=True).count()
    
    # Calculate the percentage of work done
    if total_processes > 0:
        work_done_percentage = (completed_processes / total_processes) * 100
    else:
        work_done_percentage = 0

    # Separate completed and upcoming processes
    for process_detail in process_details:
        if process_detail.completed:
            last_completed = process_detail
        else:
            upcoming_process_details.append(process_detail)

    if request.method == 'POST':
        process_id = request.POST.get('process_id')  # Assuming you have a hidden input field with the process id
        process = ProcessDetails.objects.get(pk=process_id)
        process.completed = True  # Marking the process as completed
        process.completed_time = timezone.now()  # Set the completion time
        process.save()
        entry.update_order_status()
        return redirect('display_entry_details', entry_id=entry_id)
    
    

    return render(request, 'entry_details.html', {
        'entry': entry,
        'last_completed': last_completed,
        'upcoming_process_details': upcoming_process_details,
        'total_processes': total_processes,
        'completed_processes': completed_processes,
        'work_done_percentage': work_done_percentage
    })  

def display_form_data(request):
    form_data = FormData.objects.all()
    return render(request, 'form_data_list.html', {'form_data': form_data})

#grnentry
def savegrndata1(request):
   
   if request.method== "POST":
      GRNNO=request.POST.get('GRNNO')
      MATERIALDESCRIPTION=request.POST.get('MATERIALDESCRIPTION')
      MATERIALGRADE=request.POST.get('MATERIALGRADE')
      QUANTITYTYPE=request.POST.get('QUANTITYTYPE')
      NOQUANTITY=request.POST.get('NOQUANTITY')
      STOREOWNER=request.POST.get('STOREOWNER')
      ORDERTYPE=request.POST.get('ORDERTYPE')
      PONO=request.POST.get('PONO')
      CHALLANNO=request.POST.get('CHALLANNO')
      COMMENTS=request.POST.get('COMMENTS')
      SONO=request.POST.get('SONO')
      PARTNAME=request.POST.get('PARTNAME')
      DRAWINGNO=request.POST.get('DRAWINGNO')
      EXPTIME=request.POST.get('EXPTIME')
      en= Grnentry1(grnentry_GRNNO=GRNNO,grnentry_MATERIALDESCRIPTION=MATERIALDESCRIPTION,grnentry_MATERIALGRADE=MATERIALGRADE,grnentry_QUANTITYTYPE=QUANTITYTYPE,grnentry_NOQUANTITY=NOQUANTITY,grnentry_ORDERTYPE=ORDERTYPE,grnentry_STOREOWNER=STOREOWNER,grnentry_PONO=PONO,grnentry_CHALLANNO=CHALLANNO,grnentry_COMMENTS=COMMENTS,grnentry_SONO=SONO,grnentry_PARTNAME=PARTNAME,grnentry_DRAWINGNO=DRAWINGNO,grnentry_EXPTIME=EXPTIME)
      en.save()
   return render(request,'grnentry1.html')

def serve_pdf(request, file_path):
    # Construct the absolute file path
    pdf_path = os.path.join(settings.MEDIA_ROOT, file_path)
    print("PDF Path:", pdf_path)  # Debugging statement
    
    # Check if the file exists
    if os.path.exists(pdf_path):
        # Open the file and return it as a response
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(pdf_path)
            return response
    else:
        print("PDF file not found")  # Debugging statement
        return HttpResponse("PDF file not found", status=404)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from grnentry.models import fields

@csrf_exempt
def savefield(request):
    if request.method == 'POST':
        field_name = request.POST.get('field')
        if fields.objects.filter(field=field_name).exists():
            return JsonResponse({'success': False, 'error': 'Field already exists.'})
        new_field = fields.objects.create(field=field_name)
        return JsonResponse({'success': True, 'field': new_field.field})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def savegrndata(request):
    if request.method == "POST":
        GRNNO = request.POST.get('GRNNO')
        MATERIALDESCRIPTION = request.POST.get('MATERIALDESCRIPTION')
        MATERIALGRADE = request.POST.get('MATERIALGRADE')  # Correct field name
        QUANTITYTYPE = request.POST.get('grnentry_QUANTITYTYPE')  # Correct field name
        NOQUANTITY = request.POST.get('NOQUANTITY')  # Correct field name
        STOREOWNER = request.POST.get('grnentry_STOREOWNER')  # Correct field name
        ORDERTYPE = request.POST.get('grnentry_ORDERTYPE')  # Correct field name
        PONO = request.POST.get('PONO')  # Correct field name
        CHALLANNO = request.POST.get('CHALLANNO')  # Correct field name
        COMMENTS = request.POST.get('COMMENTS')  # Correct field name
        SONO = request.POST.get('SONO')  # Correct field name
        PARTNAME = request.POST.get('PARTNAME')  # Correct field name
        DRAWINGNO = request.POST.get('DRAWINGNO')
        REVISIONNO = request.POST.get('REVISIONNO')   # Correct field name
        EXPTIME = request.POST.get('EXPTIME')  # Correct field name

        # Create an instance of your model and save it
        grn_entry = Grnentry1(
            grnentry_GRNNO=GRNNO,
            grnentry_MATERIALDESCRIPTION=MATERIALDESCRIPTION,
            grnentry_MATERIALGRADE=MATERIALGRADE,
            grnentry_QUANTITYTYPE=QUANTITYTYPE,
            grnentry_NOQUANTITY=NOQUANTITY,
            grnentry_STOREOWNER=STOREOWNER,
            grnentry_ORDERTYPE=ORDERTYPE,
            grnentry_PONO=PONO,
            grnentry_CHALLANNO=CHALLANNO,
            grnentry_COMMENTS=COMMENTS,
            grnentry_SONO=SONO,
            grnentry_PARTNAME=PARTNAME,
            grnentry_DRAWINGNO=DRAWINGNO,
            REVISIONNO=REVISIONNO,
            grnentry_EXPTIME=EXPTIME
        )
        grn_entry.save()

        

    return render(request, 'grnentry1.html')
    # If the request method is not POST, render the form template
    return render(request, 'grnentry1.html')

def field(request):
    field=fields.objects.all()
    for fieldes in field:
        print(fieldes.field)
    return render(request,'grnentry1.html',{'fields':field})   





def saveemployee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Designation = request.POST.get('Designation')
        aadhar_no = request.POST.get('aadhar_no')
        mobile_no = request.POST.get('mobile_no')

        EN=Employee_info(name=name, Designation=Designation, aadhar_no=aadhar_no, mobile_no=mobile_no)
        EN.save()

    return redirect(showemployee)

def showemployee(request):
    employees = Employee_info.objects.all()
    return render(request, 'Employees.html', {'employees': employees})

def update_employee(request, employee_id):
    if request.method == 'POST':
        employee = Employee_info.objects.get(id=employee_id)
        employee.name = request.POST.get('name')
        employee.Designation = request.POST.get('Designation')
        employee.aadhar_no = request.POST.get('aadhar_no')
        employee.mobile_no = request.POST.get('mobile_no')
        employee.save()
        return redirect(showemployee)
    else:
        employee = Employee_info.objects.get(id=employee_id)
        return render(request, 'Employee.html', {'employee': employee})


def instruction_calibration(request):
    return render(request, 'instruction_calibration.html')


def ins_cal_form(request):
    if request.method == 'POST':
        # Get data from the form
        inst_name = request.POST.get('inst_name')
        make = request.POST.get('make')
        least_count = request.POST.get('least_count')
        least_count_unit = request.POST.get('least_count_unit')
        least_range = request.POST.get('least_range')
        max_range = request.POST.get('max_range')
        range_unit = request.POST.get('range_unit')
        location = request.POST.get('location')
        calibrated_date = request.POST.get('calibrated_date')
        next_calibration_due_date = request.POST.get('next_calibration_due_date')
        remark = request.POST.get('remark')
        # Create a new calibration object
        en = calibration(
            inst_name=inst_name, make=make, least_count=least_count, least_count_unit=least_count_unit,
            least_range=least_range, max_range=max_range, range_unit=range_unit, location=location,
            calibrated_date=calibrated_date, next_calibration_due_date=next_calibration_due_date, remark=remark
        )
        en.save()
        # Redirect to show_ins_cal view
        return redirect(show_ins_cal)
    return render(request, 'instruction_calibration.html')

def mark_complete(request, pk):
    material = get_object_or_404(Outsourse, pk=pk)
    material.status = 'complete'
    material.completed_time = timezone.now()
    material.save()
    return redirect('showoutsourse')

def update_cal(request, pk):
    cal = get_object_or_404(calibration, pk=pk)
    if request.method == 'POST':
        # Update the existing calibration object
        cal.inst_name = request.POST.get('inst_name')
        cal.make = request.POST.get('make')
        cal.least_count = request.POST.get('least_count')
        cal.least_count_unit = request.POST.get('least_count_unit')
        cal.least_range = request.POST.get('least_range')
        cal.max_range = request.POST.get('max_range')
        cal.range_unit = request.POST.get('range_unit')
        cal.location = request.POST.get('location')
        cal.calibrated_date = request.POST.get('calibrated_date')
        cal.next_calibration_due_date = request.POST.get('next_calibration_due_date')
        cal.remark = request.POST.get('remark')
        cal.save()
        # Redirect to show_ins_cal view
        return redirect(show_ins_cal)
    return render(request, 'instruction_calibration.html', {'cal': cal})

def show_ins_cal(request):
    # Retrieve all calibration objects
    ins_cal = calibration.objects.all()
    return render(request, 'instruction_calibration.html', {'cal': ins_cal})

def master_component_form(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        drawing_no = request.POST.get('drawing_no')
        revision_no = request.POST.get('revision_no')
        drawing_pdf = request.POST.get('drawing_pdf')  # Correct field name
        
        en=master_component(description=description,drawing_no=drawing_no,revision_no=revision_no,drawing_pdf=drawing_pdf)
        en.save()
    return redirect(show_master_component)

def show_master_component(request):
    components=master_component.objects.all()
    for component in components:
        print(component.description)
    return render(request,'master_component.html',{'components':components})    

def update_master_component(request, component_id):
    component = get_object_or_404(master_component, id=component_id)
    if request.method == 'POST':
        component.description = request.POST.get('description')
        component.drawing_no = request.POST.get('drawing_no')
        component.revision_no = request.POST.get('revision_no')
        if request.FILES.get('drawing_pdf'):
            component.drawing_pdf = request.FILES.get('drawing_pdf')
        component.save()
        return redirect(show_master_component)
    return render(request, 'master_component.html', {'component': component})

def grninfo(request):
   grninfo=Grnentry1.objects.all()
   for elements in grninfo:
      print(elements.grnentry_QUANTITYTYPE)
   return render(request,'grnmainpage.html',{'grn':grninfo})

def display_material(request):
    materials=material.objects.all()
    for mat in materials:
        print(mat.DRAW_NO)
    return render(request,'materialinfo.html',{'materials':materials})   


def savematerial(request):
    if request.method == 'POST':
        part_description = request.POST.get('part_description')
        DRAW_NO = request.POST.get('DRAW_NO')
        Material_Grade = request.POST.get('Material_Grade')
        Finish_size = request.POST.get('Finish_size')  # Correct field name
        Raw_material_size = request.POST.get('Raw_material_size')  # Correct field name
        order_size = request.POST.get('order_size')  # Correct field name
        DRAWING_PDF = request.POST.get('DRAWING_PDF')  # Correct field name
        en=material(part_description=part_description,DRAW_NO=DRAW_NO,Material_Grade=Material_Grade,Finish_size=Finish_size,Raw_material_size=Raw_material_size,order_size=order_size,DRAWING_PDF=DRAWING_PDF)
        en.save()
        return redirect(display_material)

def get_material(request):
    material_id = request.GET.get('id')
    material_obj = get_object_or_404(material, id=material_id)
    data = {
        'id': material_obj.id,
        'part_description': material_obj.part_description,
        'DRAW_NO': material_obj.DRAW_NO,
        'Material_Grade': material_obj.Material_Grade,
        'Finish_size': material_obj.Finish_size,
        'Raw_material_size': material_obj.Raw_material_size,
        'order_size': material_obj.order_size,
        'DRAWING_PDF': material_obj.DRAWING_PDF.url,  # Adjust as per your model field
    }
    return JsonResponse(data)

def edit_material(request):
    if request.method == 'POST':
        material_id = request.POST.get('material_id')
        material_obj = get_object_or_404(material, id=material_id)
        material_obj.part_description = request.POST.get('part_description')
        material_obj.DRAW_NO = request.POST.get('DRAW_NO')
        material_obj.Material_Grade = request.POST.get('Material_Grade')
        material_obj.Finish_size = request.POST.get('Finish_size')
        material_obj.Raw_material_size = request.POST.get('Raw_material_size')
        material_obj.order_size = request.POST.get('order_size')
        if request.FILES.get('DRAWING_PDF'):
            material_obj.DRAWING_PDF = request.FILES['DRAWING_PDF']
        material_obj.save()
        return HttpResponse('Material updated successfully!')
    else:
        return HttpResponse('Invalid request method')

#inventory
def calculate_remaining_units():
    # Get all FormData objects
    form_data_list = FormData.objects.all()

    # Calculate remaining units for each FormData object
    for form_data in form_data_list:
        # Get the total quantity from the related Grnentry1 object
        total_quantity = form_data.grn_entry.grnentry_NOQUANTITY

        # Calculate total quantity dispatched
        total_dispatched_quantity = Delivery.objects.filter(form_data=form_data).aggregate(total=Sum('TTL_QNT_DISPATCH'))['total'] or 0

        # Calculate remaining units
        remaining_units = total_quantity - total_dispatched_quantity

        # Save remaining units to Inventory model
        inventory, created = Inventory.objects.get_or_create(form_data=form_data)
        inventory.remaining_quantity = remaining_units
        inventory.save()

from django.db.models import Sum, Q

from django.db.models import Sum, Q

def inventory_view(request):
    # Query all FormData objects
    form_data_list = FormData.objects.all().order_by('-dispatch_time')

    # Initialize a dictionary to store merged inventory data
    inventory_data = {}

    # Iterate through each FormData object
    for form_data in form_data_list:
        # Calculate total dispatched quantity for the current FormData object
        total_dispatched_quantity = form_data.delivery_set.aggregate(total_dispatched=Sum('TTL_QNT_DISPATCH'))['total_dispatched'] or 0

        # Get the total quantity from the related Grnentry1 object
        total_quantity = form_data.grn_entry.grnentry_NOQUANTITY

        # Calculate remaining units
        remaining_units = total_quantity - total_dispatched_quantity

        # Calculate finished quantity from deliveries
        total_finished_quantity = form_data.delivery_set.aggregate(total_finished=Sum('FINISHEDQTY'))['total_finished'] or 0

        # Calculate rejected quantity
        rejected_quantity = total_quantity - total_finished_quantity

        # Get the part name, drawing number, and material grade
        part_name = form_data.grn_entry.grnentry_PARTNAME
        drawing_no = form_data.grn_entry.grnentry_DRAWINGNO
        material_grade = form_data.grn_entry.grnentry_MATERIALGRADE

        # Create a key for the dictionary based on the drawing number
        key = drawing_no

        # Retrieve the part costs from the associated Delivery objects
        part_costs = form_data.delivery_set.values_list('PARTCOST', flat=True)

        # Update the inventory data dictionary
        if key in inventory_data:
            inventory_data[key]['remaining_quantity'] += remaining_units
            inventory_data[key]['rejected_quantity'] += rejected_quantity
            inventory_data[key]['part_costs'].extend(part_costs)
        else:
            inventory_data[key] = {
                'part_name': part_name,
                'drawing_no': drawing_no,
                'material_grade': material_grade,
                'remaining_quantity': remaining_units,
                'rejected_quantity': rejected_quantity,
                'part_costs': list(part_costs)
            }

    # Format the part costs as comma-separated values
    for key in inventory_data:
        inventory_data[key]['part_costs'] = ', '.join(map(str, set(inventory_data[key]['part_costs'])))

    # Render the inventory template with the merged inventory data
    return render(request, 'inventory.html', {'inventory_list': inventory_data.values()})

def dashboard(request):
    return render(request,'dashboard.html')

'''
def apicall_items(request):
    access_token = "1000.10842b324091f265854f6ad694586a56.d0d58b87dcf1c7dd8ea867e25a6fd36c"
    api_key = "ae530111a097e271b8c051b25b3b59c7"
    url = "https://www.zohoapis.in/books/v3/items?organization_id=60004755614"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Api-Key": api_key,
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
          salesorders = data["items"]
       
        for apiitems_data in salesorders:
                # Your code to handle each salesorder
            
            apiitems.objects.create(
                item_id=apiitems_data["item_id"],
                name=apiitems_data["name"],
                status=apiitems_data['item_name'],
                unit=apiitems_data['unit'],
                status=apiitems_data["status"],
                source=apiitems_data["source"],
                is_linked_with_zohocrm=apiitems_data["is_linked_with_zohocrm"],
                  zcrm_product_id=apiitems_data["zcrm_product_id"],
                  description=apiitems_data["description"],
                  rate=apiitems_data["rate"],
                  tax_id=apiitems_data["tax_id"],
                  item_tax_preferences_tax_specification=apiitems_data["item_tax_preferences"],
                  item_tax_preferences_tax_name_formatted=apiitems_data[],
                  item_tax_preferences_tax_type=apiitems_data[],
                  item_tax_preferences_tax_name=apiitems_data[],
                  item_tax_preferences_tax_percentage=apiitems_data[],
                  item_tax_preferences_tax_id=apiitems_data[],
                  item_tax_preferences_tax_specification2=apiitems_data[],
                  item_tax_preferences_tax_name_formatted2=apiitems_data[],
                  item_tax_preferences_tax_type2=apiitems_data[],
                  item_tax_preferences_tax_name2=apiitems_data[],
                  item_tax_preferences_tax_percentage2=apiitems_data[],
                  item_tax_preferences_tax_id2=apiitems_data[],
                  tax_name=apiitems_data[],
                  tax_percentage=apiitems_data[],
                  purchase_account_id=apiitems_data[],
                  purchase_account_name=apiitems_data[],
                  account_id=apiitems_data[],
                  account_name=apiitems_data[],
                  purchase_description=apiitems_data[],
                  purchase_rate=apiitems_data[],
                  item_type=apiitems_data[],
                  product_type=apiitems_data[],
                  is_taxable=apiitems_data[],
                  tax_exemption_id=apiitems_data[],
                  tax_exemption_code=apiitems_data[],
                  has_attachment=apiitems_data[],
                  sku=apiitems_data[],
                  image_name=apiitems_data[],
                  image_type=apiitems_data[],
                  image_document_id=apiitems_data[],
                  created_time=apiitems_data[],
                  last_modified_time=apiitems_data[],
                  hsn_or_sac=apiitems_data[],
                  cf_design_hours=apiitems_data[],
                  cf_design_hours_unformatted=apiitems_data[]
                print("saved")
            return JsonResponse({"message": "Data saved successfully."})
            )
        
    else:
        error_data = {
            "error": f"Error: {response.status_code}",
            "error_message": response.text,
        }
        return JsonResponse(error_data, status=response.status_code) 
'''


#function for salesorder for api
def apicall_salesorder(request):
    token = "1000.de2dbd5217619fc816b1f608078e4902.7df2bbaa1f90bb99bb199ff14d8b0adaf"
    api_key = "ae530111a097e271b8c051b25b3b59c7"
    url = "https://www.zohoapis.in/books/v3/salesorders?organization_id=60004755614"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Api-Key": api_key,
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
       
        if "salesorders" in data:
            salesorders = data["salesorders"]
       
            for salesorder_data in salesorders:
                # Check if the salesorder_id already exists in the database
                if not salesorder.objects.filter(salesorder_id=salesorder_data["salesorder_id"]).exists():
                    salesorder.objects.create(
                        salesorder_id=salesorder_data["salesorder_id"],
                        zcrm_potential_id=salesorder_data["zcrm_potential_id"],
                        zcrm_potential_name=salesorder_data["zcrm_potential_name"],
                        customer_name=salesorder_data["customer_name"],
                        customer_id=salesorder_data["customer_id"],
                        email=salesorder_data["email"],
                        delivery_date=salesorder_data["delivery_date"],
                        company_name=salesorder_data["company_name"],
                        color_code=salesorder_data["color_code"],
                        current_sub_status_id=salesorder_data["current_sub_status_id"],
                        current_sub_status=salesorder_data["current_sub_status"],
                        pickup_location_id=salesorder_data["pickup_location_id"],
                        salesorder_number=salesorder_data["salesorder_number"],
                        reference_number=salesorder_data["reference_number"],
                        date=salesorder_data["date"],
                        shipment_date=salesorder_data["shipment_date"],
                        shipment_days=salesorder_data["shipment_days"],
                        due_by_days=salesorder_data["due_by_days"],
                        due_in_days=salesorder_data["due_in_days"],
                        currency_id=salesorder_data["currency_id"],
                        source=salesorder_data["source"],
                        currency_code=salesorder_data["currency_code"],
                        total=salesorder_data["total"],
                        bcy_total=salesorder_data["bcy_total"],
                        total_invoiced_amount=salesorder_data["total_invoiced_amount"],
                        created_time=salesorder_data["created_time"],
                        last_modified_time=salesorder_data["last_modified_time"],
                        is_emailed=salesorder_data["is_emailed"],
                        quantity_invoiced=salesorder_data["quantity_invoiced"],
                        order_status=salesorder_data["order_status"],
                        invoiced_status=salesorder_data["invoiced_status"],
                        paid_status=salesorder_data["paid_status"],
                        status=salesorder_data["status"],
                        salesperson_name=salesorder_data["salesperson_name"],
                        branch_id=salesorder_data["branch_id"],
                        branch_name=salesorder_data["branch_name"],
                        has_attachment=salesorder_data["has_attachment"],
                        custom_fields_list=salesorder_data["custom_fields_list"],
                        delivery_method=salesorder_data["delivery_method"],
                        delivery_method_id=salesorder_data["delivery_method_id"])
                    print("saved")
                else:
                    print(f"Sales order with ID {salesorder_data['salesorder_id']} already exists.")
                    
        return JsonResponse({"message": "Data processed successfully."})   
    else:
        error_data = {
            "error": f"Error: {response.status_code}",
            "error_message": response.text,
        }
        print("Error in API request:", error_data)
        return JsonResponse(error_data, status=response.status_code)

def salesorderinfo(request):
   salesorderinfo=salesorder.objects.all().order_by('-date')
   for elements in salesorderinfo:
      print(elements.customer_name)
   return render(request,'salesorder.html',{'sales':salesorderinfo})

def field(request):
    field=fields.objects.all()
    for fieldes in field:
        print(fieldes.field)
    return render(request,'grnentry1.html',{'fields':field})    


#purchaseorder functions for api
def apicall_purchaseorder(request):
    access_token = "1000.1b2970bb4835a26c56535ddd9142a525.a7e5d78ef91106088fc7beeaa49c012a"
    api_key = "ae530111a097e271b8c051b25b3b59c7"
    url = "https://www.zohoapis.in/books/v3/purchaseorders?organization_id=60004755614"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Api-Key": api_key,
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        if "purchaseorders" in data:
          purchaseorder = data["purchaseorders"]
       
        for purchaseorder_data in purchaseorder:
            apipurchaseorder.objects.create(
                purchaseorder_id=purchaseorder_data["purchaseorder_id"],
                vendor_id=purchaseorder_data["vendor_id"],
                vendor_name=purchaseorder_data["vendor_name"],
                company_name=purchaseorder_data["company_name"],
                order_status=purchaseorder_data["order_status"],
                billed_status=purchaseorder_data["billed_status"],
                status=purchaseorder_data["status"],
                color_code=purchaseorder_data["color_code"],
                current_sub_status_id=purchaseorder_data["current_sub_status_id"],
                current_sub_status=purchaseorder_data["current_sub_status"],
                purchaseorder_number=purchaseorder_data["purchaseorder_number"],
                reference_number=purchaseorder_data["reference_number"],
                date=purchaseorder_data["date"],
                delivery_date=purchaseorder_data["delivery_date"],
                delivery_days=purchaseorder_data["delivery_days"],
                due_by_days=purchaseorder_data["due_by_days"],
                due_in_days=purchaseorder_data["due_in_days"],
                currency_id=purchaseorder_data["currency_id"],
                currency_code=purchaseorder_data["currency_code"],
                price_precision=purchaseorder_data["price_precision"],
                total= purchaseorder_data["total"],
                has_attachment=purchaseorder_data["has_attachment"],
                created_time=purchaseorder_data["created_time"],
                last_modified_time=purchaseorder_data["last_modified_time"],
                quantity_yet_to_receive=purchaseorder_data["quantity_yet_to_receive"],
                quantity_marked_as_received=purchaseorder_data["quantity_marked_as_received"],
                receives=purchaseorder_data["receives"],
                client_viewed_time=purchaseorder_data["client_viewed_time"],
                is_viewed_by_client=purchaseorder_data["is_viewed_by_client"],
                branch_id=purchaseorder_data["branch_id"],
                branch_name=purchaseorder_data["branch_name"])
            print("saved")
        return JsonResponse({"message": "Data saved successfully."})
    else:
        error_data = {
            "error": f"Error: {response.status_code}",
            "error_message": response.text,
        }
        return JsonResponse(error_data, status=response.status_code) 
def purchaseinfo(request):
   purchaseinfo=apipurchaseorder.objects.all().order_by('-date')
   print(purchaseinfo)
   for elements in purchaseinfo:
      print(elements.vendor_name)
   return render(request,'purchaseorder1.html',{'purchase':purchaseinfo})



def purchaseentryshow1(request):
    return render(request,'purchaseentryshow.html')


