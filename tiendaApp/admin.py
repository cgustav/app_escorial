from django.contrib import admin
from django.contrib.auth.models import Permission
from tiendaApp.models import Tipo,Repuesto

# Registrar Permission
admin.site.register(Permission)

@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'creado']
    search_fields = ['nombre']

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
