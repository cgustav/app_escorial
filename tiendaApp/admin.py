from django.contrib import admin

# Register your models here.
from tiendaApp.models import Tipo,Repuesto

@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'creado']
    search_fields = ['nombre']

# class CantidadAdmin(admin.ModelAdmin):
#     list_display = ['nombre']

@admin.register(Repuesto)
class RepuestoAdmin(admin.ModelAdmin):
    list_display = [
        'codigoRepuesto', 
        'nombre', 
        'tipo', 
        'precio', 
        'stock',  # Cambia 'cantidad' por 'stock'
        'creado'
    ]
    list_filter = ['tipo']
    search_fields = ['nombre', 'codigoRepuesto']
    readonly_fields = ['codigoRepuesto', 'stock', 'creado']
    ordering = ['nombre']


# admin.site.register(Tipo,TipoAdmin)
# admin.site.register(Cantidad,CantidadAdmin)
# admin.site.register(Repuesto,RepuestoAdmin)