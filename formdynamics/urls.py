"""
URL configuration for formdynamics project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import master_component_form, show_master_component, update_master_component

urlpatterns = [
    path('admin/', admin.site.urls),
    path('grnentry1',views.grnentry, name='grnentry'),
    path('grnentry',views.savegrndata,name='savegrndata'),
    path('grnmainpage',views.grninfo,name='grninfo'),
    path('apicall_salesorder',views.apicall_salesorder,name='apicall'),
    path('apicall_purchaseorder',views.apicall_purchaseorder,name='apicall_purchaseorder'),
    path('salesorder1',views.salesorderinfo),
    path('purchaseinfo',views.purchaseinfo),
    path('',views.home,name="home"),  
    path("purchaseinfo",views.purchaseinfo),
    path("purchaseinfoshow",views.purchaseinfoshow),
    path('trackentry',views.trackentry),
    path('inventory',views.inventory_view,name='inventory'),
    path('trackmainpage',views.trackmainpage),
    path('purchaseentryshow',views.purchaseentryshow1),
    path('dispatch_details/<int:entry_id>/', views.dispatch_details, name='dispatch_details'),
    path('delivery_success/', views.delivery_success, name='delivery_success'),
    path('form/',views.form_view, name='form_view'),  # URL for the form page
    path('displayformdata',views.display_form_data, name='display_form_data'),
    path('display_form_data', views.display_form_data, name='display_form_data'),
    path('entry_details<int:entry_id>', views.display_entry_details, name='display_entry_details'),
    path('form-view<int:entry_id>', views.form_view1, name='form_view1'),
    path('field',views.field,name='field'),
    path("field",views.savefield,name='savefield'),
    path('savefield/', views.savefield, name='savefield'),
    path('materialinfo1',views.display_material,name='display_material'),
     path('get_material/', views.get_material, name='get_material'),
    path('edit_material/', views.edit_material, name='editmaterial'),
    # URL for editing material (POST request)
    path('edit_material/', views.edit_material, name='edit_material'),

    path('savematerial',views.savematerial,name='savematerial'),
    path('saveemployee/', views.saveemployee, name='saveemployee'),
    
    # URL pattern for displaying all employees
   path('employees', views.showemployee),
    path('update_employee/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('saveemployee/', views.saveemployee, name='saveemployee'),

 # URL for showing instruction calibration page
     path('instruction_calibration', views.show_ins_cal),
    # URL for adding new calibration instruction
    path('cal/', views.ins_cal_form, name='cal'),
    # URL for updating existing calibration instruction
    path('update_cal/<int:pk>/', views.update_cal, name='update_cal'),
   



   path('show_master_component',views.show_master_component,name='show_master_component'),
   path('master_component_form',views.master_component_form,name='master_component_form'),
   path('update_master_component/<int:component_id>/', views.update_master_component, name='update_master_component'),
   path('pdf/<path:file_path>/', views.serve_pdf, name='serve_pdf'),

    path('outsourse',views.outsourse),
    path('showoutsourse',views.showoutsourse,name='showoutsourse'),
    path('outsourseform',views.outsourseform,name='outsourseform'),
    path('mark_complete/<int:pk>/', views.mark_complete, name='mark_complete'),

       path('notifications/', views.get_notifications, name='notifications'),
    
     

] 
