from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import Avatar, Message



class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'
        


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['image']
        labels = {'image': 'Imagen'}



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message

        fields = ['name', 'email', 'phone', 'content'] 
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre y apellido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'phone': forms.NumberInput(attrs={'placeholder': 'Teléfono'}),
            'content': forms.Textarea(attrs={'placeholder': 'Mensaje'})
        }
        labels = {
            'name': 'Nombre y apellido',
            'email': 'Correo electrónico',
            'phone': 'Teléfono',
            'content': 'Mensaje'
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        words = name.split()
        if len(words) < 2:
            raise ValidationError("Ingresa tu nombre y apellido correctamente.")
        return name