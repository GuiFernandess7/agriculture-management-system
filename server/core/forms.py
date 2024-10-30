from django import forms
from core.models import Field

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ('name', 'area', 'lon', 'lat', 'soil_type')  # Corrigido para uma tupla simples
        labels = {
            'name': 'Nome',
            'lon': 'Longitude',
            'lat': 'Latitude',
            'area': 'Área',
            'soil_type': 'Tipo de Solo',
        }
