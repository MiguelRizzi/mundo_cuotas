from django import forms
from .models import Product
from multiupload.fields import MultiFileField

class ProductForm(forms.ModelForm):
    files = MultiFileField(min_num=1, max_num=10, label='Archivos a agregar', required=False)

    class Meta:
        model = Product
        fields = ['name', 'category', 'price_cost', 'price_cash', 'type', 'status', 'description']
        labels = {
            'name': 'Nombre', 
            'description': 'Descripción',
            'price_cost': 'Precio de costo', 
            'price_cash': 'Precio de contado', 
            'type': 'Tipo', 
            'status': 'Estado', 
            'category': 'Categoría'
        }
        


