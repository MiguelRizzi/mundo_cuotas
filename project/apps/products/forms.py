from django import forms
from .models import Product
from multiupload.fields import MultiFileField

class BaseProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'description']
        labels = {'name': 'Nombre', 'description': 'Descripción', 'price': 'Precio de contado', 'category': 'Categoría'}

class ProductForm(BaseProductForm):
    files = MultiFileField(min_num=1, max_num=10, label='Archivos a agregar')
    # existent_files = forms.MultipleChoiceField(choices=[], label='Selecciona archivos a eliminar')

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['existent_files'].choices = [(f.id, f.file) for f in self.instance.files.all()]
    """

class ProductUpdateForm(BaseProductForm):
    pass