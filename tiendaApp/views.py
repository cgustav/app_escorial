from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from tiendaApp.forms import RepuestoForm, SearchForm, PedidoForm, PedidoItemForm, PedidoSearchForm, StockOperationForm,StockOperationSearchForm
from django.contrib import messages
from tiendaApp.models import Repuesto,Tipo, Pedido, PedidoItem, StockOperation
from .forms import SearchForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from ipware import get_client_ip
import logging

logger = logging.getLogger(__name__)

def staff_check(user):
    return user.is_staff

# Create your views here.
def inicio(request):
    return render(request,'tiendaTemplates/inicio.html')

# Importa HttpResponse para manejar la respuesta HTTP
@login_required
@user_passes_test(staff_check, login_url='login')
def crear_repuesto(request):
    if request.method == 'POST':
        form = RepuestoForm(request.POST,request.FILES)
        if form.is_valid():
            repuesto = form.save(commit=False)
            
            # Manejar la imagen
            if 'fotografia' in request.FILES:
                repuesto.fotografia = request.FILES['fotografia']
            else:
                repuesto.fotografia = 'repuestos/tractor.png'

            repuesto.save()
            messages.success(request, 'Repuesto creado exitosamente')

            return redirect('repuestos')  # Cambia 'repuestos' con la URL a la que quieras redirigir después de crear el repuesto
    else:
        form = RepuestoForm()

    return render(request, 'tiendaTemplates/repuestoAdd.html', {'form': form})

@login_required
@user_passes_test(staff_check, login_url='login')
def todos_repuesto(request):
    
    # Utilidades de busqueda
    query = request.GET.get('query', '')
    tipo_seleccionado = request.GET.get('tipo')
    orden = request.GET.get('orden', 'nombre')
    
    if query:
        repuestos = Repuesto.buscar(query)
    else:
        repuestos = Repuesto.objects.all()
    
    
    repuestos = Repuesto.aplicar_filtros(
        repuestos, 
        tipo=tipo_seleccionado, 
        orden=orden
    )
    

    # Paginador de repuestos
    paginator = Paginator(repuestos, 10)  # 10 items por página
    page_obj = paginator.get_page(request.GET.get('page'))


    tipos = Tipo.objects.all()
    
    # Código de búsqueda
    query = None
    results = []

    # form = SearchForm(initial={'query': query})
    # Preparar el formulario con los valores actuales
    form = SearchForm(initial={
        'query': query,
        'tipo': tipo_seleccionado,
        'orden': orden
    })
    
    data = {
        'page_obj': page_obj,
        'repuestos': repuestos,
        'tipos': tipos,
        # 'cantidades': cantidades,
        'form': form,
        'query': query,
        'results': repuestos,  # Puedes personalizar esto según tu lógica de búsqueda
    }

    return render(request, 'tiendaTemplates/repuestos.html', data)

@login_required
@user_passes_test(staff_check, login_url='login')
def cargar_editar_repuesto(request,repuesto_id):
    repuesto = get_object_or_404(Repuesto,id=repuesto_id)
    form = RepuestoForm(instance=repuesto)

    return render(request, 'tiendaTemplates/repuestoEdit.html', {'form':form,'repuesto':repuesto})

@login_required
@user_passes_test(staff_check, login_url='login')
def editar_repuesto(request,repuesto_id):
    repuesto = get_object_or_404(Repuesto,id=repuesto_id)

    if request.method == 'POST':
        form = RepuestoForm(request.POST, request.FILES, instance=repuesto)
        if form.is_valid():
            repuesto = form.save(commit=False)
            
            if 'fotografia' in request.FILES:
                # Si hay una nueva imagen, S3 automáticamente sobrescribirá la anterior
                repuesto.fotografia = request.FILES['fotografia']
            elif not repuesto.fotografia:
                # Si no hay imagen y tampoco había una antes, usar la imagen por defecto
                repuesto.fotografia = 'repuestos/tractor.png'
                
            repuesto.save()
            messages.success(request, 'Repuesto actualizado exitosamente')
            
            return redirect('repuestos')
    else:
        form = RepuestoForm(instance=repuesto)

    return render(request, 'tiendaTemplates/repuestoEdit.html', {
        'form':form,
        'repuesto': repuesto
    })

@login_required
@user_passes_test(staff_check, login_url='login')
def desactivar_repuesto(request, repuesto_id):
    repuesto = get_object_or_404(Repuesto, id=repuesto_id)
    if repuesto.activo:
        repuesto.activo = False
        repuesto.save()
        messages.success(request, f"El repuesto {repuesto.nombre} ha sido desactivado.")
    else:
        messages.info(request, f"El repuesto {repuesto.nombre} ya estaba desactivado.")
    return redirect('repuestos')

@login_required
@user_passes_test(staff_check, login_url='login')
def activar_repuesto(request, repuesto_id):
    repuesto = get_object_or_404(Repuesto, id=repuesto_id)
    if not repuesto.activo:
        repuesto.activo = True
        repuesto.save()
        messages.success(request, f"El repuesto {repuesto.nombre} ha sido activado.")
    else:
        messages.info(request, f"El repuesto {repuesto.nombre} ya estaba activo.")
    return redirect('repuestos')


@login_required
@user_passes_test(staff_check)
def registro_operacion_stock(request, tipo_operacion):
    if tipo_operacion not in ['INGRESO', 'MERMA']:
        messages.error(request, "Tipo de operación inválida")
        return redirect('lista_operaciones_stock')
        
    if request.method == 'POST':
        client_ip, _ = get_client_ip(request)
        form = StockOperationForm(
            request.POST, 
            tipo_operacion=tipo_operacion,
            user=request.user,
            ip_address=client_ip or '0.0.0.0'
        )
        
        if form.is_valid():
            try:
                operacion = form.save()
                messages.success(
                    request, 
                    f"{'Ingreso' if tipo_operacion == 'INGRESO' else 'Merma'} registrado exitosamente"
                )
                return redirect('lista_operaciones_stock')
            except ValidationError as e:
                messages.error(request, str(e))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = StockOperationForm()
    
    # Filtrar los repuestos según el tipo de operación
    if tipo_operacion == 'MERMA':
        # Para mermas, solo mostrar repuestos con stock > 0
        form.fields['repuesto'].queryset = Repuesto.activos.filter(stock__gt=0)
    
    context = {
        'form': form,
        'tipo_operacion': tipo_operacion,
        'titulo': 'Ingreso de Existencias' if tipo_operacion == 'INGRESO' else 'Registro de Merma',
        'es_ingreso': tipo_operacion == 'INGRESO'
    }
    
    return render(request, 'stock/registro_operacion.html', context)

@login_required
@user_passes_test(staff_check)
def lista_operaciones_stock(request):
    form = StockOperationSearchForm(request.GET)
    operaciones = StockOperation.objects.all()
    # operaciones = StockOperation.objects.select_related('repuesto', 'usuario').all()
    
    
    # Aplicar filtros
    if form.is_valid():
        query = form.cleaned_data.get('query')
        tipo_operacion = form.cleaned_data.get('tipo_operacion')
        fecha_desde = form.cleaned_data.get('fecha_desde')
        fecha_hasta = form.cleaned_data.get('fecha_hasta')

        operaciones = StockOperation.buscar(
            query=query,
            tipo_operacion=tipo_operacion,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta
        )
        
    # Paginación
    paginator = Paginator(operaciones, 10)  # 10 items por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'operaciones': page_obj,
        'page_obj': page_obj,
        'total_registros': operaciones.count(),
        'query_params': request.GET.urlencode()
    }
    
    return render(request, 'stock/lista_operaciones.html', context)

    
@login_required
@user_passes_test(staff_check)
def lista_pedidos(request):
    # Obtener parámetros de búsqueda y filtrado
    query = request.GET.get('query', '')
    estado = request.GET.get('estado')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    orden = request.GET.get('orden', '-fecha_creacion')

    # Realizar búsqueda
    if query:
        pedidos = Pedido.buscar(query)
    else:
        pedidos = Pedido.objects.all()
    
    # Aplicar filtros
    pedidos = Pedido.aplicar_filtros(
        pedidos,
        estado=estado,
        orden=orden,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
    
    # Paginación
    paginator = Paginator(pedidos, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    # Preparar formulario
    form = PedidoSearchForm(initial={
        'query': query,
        'estado': estado,
        'orden': orden,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta
    })
    
    return render(request, 'pedidos/lista_pedidos.html', {
        'form': form,
        'page_obj': page_obj,
        'pedidos': page_obj,
        'query': query
    })
    
@login_required
@user_passes_test(staff_check)
def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.creado_por = request.user
            pedido.save()
            messages.success(request, 'Pedido creado exitosamente')
            return redirect('detalle_pedido', pedido_id=pedido.id)
    else:
        form = PedidoForm()
    
    return render(request, 'pedidos/crear_pedido.html', {
        'form': form
    })
    
@login_required
@user_passes_test(staff_check)
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    items = pedido.items.all()
    
    if request.method == 'POST':
        form = PedidoItemForm(request.POST)
        if form.is_valid():
            try:
                item = form.save(commit=False)
                item.pedido = pedido
                item.save()
                messages.success(request, 'Item agregado al pedido')
                return redirect('detalle_pedido', pedido_id=pedido.id)
            except ValidationError as e:
                messages.error(request, e.message)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PedidoItemForm()

    total = pedido.calcular_total()
    
    return render(request, 'pedidos/detalle_pedido.html', {
        'pedido': pedido,
        'items': items,
        'form': form,
        'total': total
    })
    
@login_required
@user_passes_test(staff_check)
def eliminar_item_pedido(request, item_id):
    item = get_object_or_404(PedidoItem, id=item_id)
    pedido_id = item.pedido.id
    
    logger.info(f"Item ID: {item_id}, Cantidad: {item.cantidad}, Stock actual: {item.repuesto.stock}")

    try:
        if item.pedido.estado == 'CANCELADO':
            raise ValidationError("No se pueden eliminar items de un pedido cancelado")
            
        # Restaurar stock y registrar operación si el pedido no está cancelado
        if item.pedido.estado != 'CANCELADO':
            item.delete()
            messages.success(request, 'Item eliminado del pedido')
        
    except ValidationError as e:
        messages.error(request, str(e))
        
    return redirect('detalle_pedido', pedido_id=pedido_id)

@login_required
@user_passes_test(staff_check)
def cambiar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Pedido.ESTADO_CHOICES):
            if nuevo_estado == 'CANCELADO':
                client_ip, _ = get_client_ip(request)
                pedido.cancelar_pedido(request.user, client_ip)
                messages.warning(request, 'Pedido cancelado y stock restituido')
            else:
                pedido.estado = nuevo_estado
                pedido.save()
                messages.success(request, 'Estado del pedido actualizado')
    
    return redirect('detalle_pedido', pedido_id=pedido_id)