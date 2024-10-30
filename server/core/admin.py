from django import forms
from django.contrib import admin
from core.models import (
    Field,
    CropSeason,
    Harvest
)
from core.forms import FieldForm

admin.site.site_header = "AgriManager Admin"
admin.site.site_title = "AgriManager Admin"

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ['name', 'area', 'soil_type', 'location']
    fields = (('name', 'area'), 'lon', 'lat', 'soil_type')

admin.site.register(CropSeason)
admin.site.register(Harvest)
