"""
URL configuration for NegocioModel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from tiendaApp import views as vistas
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth.decorators import login_required, staff_member_required
# from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

from django.http import HttpResponse

# Crear un decorador personalizado para staff
# def staff_member_required(view_func):
#     decorated_view = user_passes_test(
#         lambda u: u.is_active and u.is_staff,
#         login_url='login'
#     )(view_func)
#     return decorated_view


def health_check(request):
    return HttpResponse("OK")

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('',vistas.inicio,name='inicio'),

    # REPUESTOS
    # ===================
    path('repuestos/', vistas.todos_repuesto, name='repuestos'),
    path('repuestoAdd/', vistas.crear_repuesto, name='crearRepuestos'),
    path('repuestoEdit/<int:repuesto_id>/', vistas.cargar_editar_repuesto, name='editarRepuesto'),
    path('repuestoEditado/<int:repuesto_id>/', vistas.editar_repuesto, name='repuestoEditado'),
    
    path('repuesto/<int:repuesto_id>/desactivar/', vistas.desactivar_repuesto, name='desactivarRepuesto'),
    path('repuesto/<int:repuesto_id>/activar/', vistas.activar_repuesto, name='activarRepuesto'),
    
    # STOCK
    # ===================
    path('stock/operacion/<str:tipo_operacion>/', vistas.registro_operacion_stock, name='registro_operacion_stock'),
    path('stock/operaciones/', vistas.lista_operaciones_stock, name='lista_operaciones_stock'),
    
    # PEDIDOS
    # ===================
    path('pedidos/', vistas.lista_pedidos, name='lista_pedidos'),
    path('pedidos/crear/', vistas.crear_pedido, name='crear_pedido'),
    path('pedidos/<int:pedido_id>/', vistas.detalle_pedido, name='detalle_pedido'),
    path('pedidos/item/<int:item_id>/eliminar/', vistas.eliminar_item_pedido, name='eliminar_item_pedido'),
    path('pedidos/<int:pedido_id>/estado/', vistas.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    
    # ADMIN
    # ===================
    path('accounts/',include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)