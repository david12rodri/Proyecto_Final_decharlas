#Descripcion: Formulario para el cambio de fuente y tamaño de letra

from django import forms
from .models import User

class Font_Formulario(forms.ModelForm):
    class Meta:
        model = User
        fields = ('font_type', 'font_size')
