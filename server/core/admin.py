from django.contrib import admin
from core.models import (
    Field,
    CropSeason,
    Harvest
)
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

admin.site.site_header = "AgriTrack Dashboard"
admin.site.site_title = "AgriTrack Dashboard"

class AreaFilter(admin.SimpleListFilter):
    title = _('Filtro de Área')
    parameter_name = 'area_filter'
    ha = 100

    def lookups(self, request, model_admin):
        return (
            ('maior', _(f'> {self.ha} ha')),
            ('menor', _(f'< {self.ha} ha')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'maior':
            return queryset.filter(area__gt=self.ha)
        if self.value() == 'menor':
            return queryset.filter(area__lt=self.ha)
        return queryset

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ['name', 'area', 'soil_type']
    fields = (('name', 'area'), 'lon', 'lat', 'soil_type', 'field_image', )
    list_editable = ('area',)
    list_filter = (AreaFilter, 'soil_type',)
    search_fields = ('name', 'soil_type',)
    ordering = ('name',)
    list_per_page = 10

    def field_image(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.field_image.url))

    field_image.short_description = 'Image'

    def get_ordering(self, request):
        if request.user.is_superuser:
            return ('name',)
        else:
            return ('-price',)

@admin.register(CropSeason)
class CropSeasonAdmin(admin.ModelAdmin):
    list_display = ['crop_type', 'start_date', 'end_date', 'location']
    search_fields = ('crop_type',)
    list_filter = ('crop_type',)
    autocomplete_fields = ('location',)
    raw_id_fields = ('location',)

@admin.register(Harvest)
class HarvestAdmin(admin.ModelAdmin):
    list_display = ['harvest_date']
