from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from daterange_filter.filter import DateRangeFilter

from .models import Lead, Colectivo


def marcar_enviado_en_csv(modeladmin, request, queryset):
    queryset.update(enviado_en_csv=True)
marcar_enviado_en_csv.short_description = "Marcar como Enviado en CSV"


def marcar_cupon_enviado(modeladmin, request, queryset):
    queryset.update(enviado_cupon=True)
marcar_cupon_enviado.short_description = "Marcar como Cupon Enviado"


def marcar_colectivo_validado(modeladmin, request, queryset):
    queryset.update(colectivo_validado=True)
marcar_colectivo_validado.short_description = "Marcar como Colectivo Validado"


def marcar_colectivo_no_validado(modeladmin, request, queryset):
    queryset.update(colectivo_validado=False)
marcar_colectivo_no_validado.short_description = "Marcar como Colectivo NO Validado"


def enviar_email_con_cupon(modeladmin, request, queryset):
    pass
enviar_email_con_cupon.short_description = "ENVIAR CUPON POR EMAIL"


class LeadResource(resources.ModelResource):

    class Meta:
        model = Lead
        list_display = ['nombre', 'primer_apellido', 'segundo_apellido', 'email', 'codigo_postal', 'enviado_en_csv', 'enviado_cupon', 'colectivo', 'colectivo_validado', ]


class LeadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombre', 'primer_apellido', 'segundo_apellido', 'email', ]
    list_filter = ['colectivo', 'colectivo_validado', 'enviado_en_csv', 'enviado_cupon', ('created', DateRangeFilter), ('updated', DateRangeFilter), ]
    list_display = ['created', 'updated', 'nombre', 'primer_apellido', 'segundo_apellido', 'email', 'codigo_postal', 'enviado_en_csv', 'enviado_cupon', 'colectivo', 'colectivo_validado', 'acreditacion', ]
    actions = [
        marcar_enviado_en_csv,
        marcar_cupon_enviado,
        marcar_colectivo_validado,
        marcar_colectivo_no_validado,
        enviar_email_con_cupon,
    ]
    resource_class = LeadResource


class ColectivoAdmin(admin.ModelAdmin):
    list_display = ['nombre', ]


admin.site.register(Lead, LeadAdmin)
admin.site.register(Colectivo, ColectivoAdmin)
