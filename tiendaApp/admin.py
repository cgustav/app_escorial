from django.contrib import admin

# Register your models here.
from tiendaApp.models import Tipo,Cantidad,Repuesto

class TipoAdmin(admin.ModelAdmin):
    list_display = ['id','nombre']

class CantidadAdmin(admin.ModelAdmin):
    list_display = ['nombre']

class RepuestoAdmin(admin.ModelAdmin):
    list_display = ['codigoRepuesto','nombre','tipo','fotografia',
                    'precio','cantidad']

admin.site.register(Tipo,TipoAdmin)
admin.site.register(Cantidad,CantidadAdmin)
admin.site.register(Repuesto,RepuestoAdmin)