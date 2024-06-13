from django import forms
from grnentry.models import Grnentry1,FormData, ProcessDetails,Delivery

class CompleteProcessForm(forms.Form):
    process_id = forms.ModelChoiceField(queryset=ProcessDetails.objects.filter(completed=False))


# forms.py


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['SOORDER', 'FINISHEDQTY', 'PDIREPORT', 'TTL_QNT_DISPATCH', 'INVOICENO', 'CUSTOMERNAME', 'BUYERNAME', 'SALESREPRESENT', 'PARTCOST']

class FormDataForm(forms.ModelForm):
    class Meta:
        model = FormData
        fields = '__all__'

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['SOORDER', 'FINISHEDQTY', 'PDIREPORT', 'TTL_QNT_DISPATCH', 'INVOICENO', 'CUSTOMERNAME', 'BUYERNAME', 'SALESREPRESENT', 'PARTCOST']        


from django import forms
from grnentry.models import material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = material
        fields = ['part_description', 'DRAW_NO', 'Material_Grade', 'Finish_size', 'Raw_material_size', 'order_size', 'DRAWING_PDF']
