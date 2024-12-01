from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from tiendaApp.forms import RepuestoForm, SearchForm, PedidoForm, PedidoItemForm, PedidoSearchForm
from django.contrib import messages
from tiendaApp.models import Repuesto,Tipo, Pedido, PedidoItem
from .forms import SearchForm
from django.core.paginator import Paginator
# from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError


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

            # Verificar si se proporcionó una nueva imagen
            # if not repuesto.fotografia:
            #     repuesto.fotografia = 'media/tractor.png'
            
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
    
    
    # Aplicar filtro por tipo independientemente de la query
    # tipo_seleccionado = request.GET.get('tipo')
    # if tipo_seleccionado:
    #     repuestos = repuestos.filter(tipo_id=tipo_seleccionado)
    
    # # Aplicar ordenamiento independientemente de la query
    # orden = request.GET.get('orden', 'nombre')
    # if orden:
    #     if orden in ['-precio', 'precio', '-nombre', 'nombre']:
    #         repuestos = repuestos.order_by(orden)
    
    
    # Ordenar los resultados
    # orden = request.GET.get('orden', 'nombre')
    # if orden:
    #     if orden == '-precio':
    #         repuestos = repuestos.order_by(orden)
    #     else:
    #         repuestos = repuestos.order_by('nombre')
    

    # Paginador de repuestos
    paginator = Paginator(repuestos, 10)  # 10 items por página
    page_obj = paginator.get_page(request.GET.get('page'))


    tipos = Tipo.objects.all()
    # tipo_seleccionado = request.GET.get('tipo')
    
    # if tipo_seleccionado:
    #     repuestos = repuestos.filter(tipo_id=tipo_seleccionado)

    # cantidades = Cantidad.objects.all()
    
    # Código de búsqueda
    query = None
    results = []

    # if 'query' in request.GET:
    #     form = SearchForm(request.GET)
    #     if form.is_valid():
    #         query = form.cleaned_data['query']
    #         repuestos = Repuesto.objects.filter(nombre__icontains=query)
    # else:
    #     form = SearchForm()


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
def eliminar_repuesto(request, repuesto_id):
    repuesto = get_object_or_404(Repuesto, id=repuesto_id)

    if request.method == 'POST':
        repuesto.delete()
        return redirect('/repuestos/')

    return render(request, 'tiendaTemplates/repuestoDel.html', {'repuesto':repuesto})


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
        
    # pedidos = Pedido.objects.all().order_by('-fecha_creacion')
    # return render(request, 'pedidos/lista_pedidos.html', {
    #     'pedidos': pedidos
    # })
    
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
    
    # Restaurar el stock
    stock_actual = item.repuesto.cantidad.get_valor_numerico()
    nuevo_stock = str(stock_actual + item.cantidad)
    item.repuesto.cantidad.nombre = nuevo_stock
    item.repuesto.cantidad.save()
    
    item.delete()
    messages.success(request, 'Item eliminado del pedido')
    return redirect('detalle_pedido', pedido_id=pedido_id)

@login_required
@user_passes_test(staff_check)
def cambiar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Pedido.ESTADO_CHOICES):
            pedido.estado = nuevo_estado
            pedido.save()
            messages.success(request, 'Estado del pedido actualizado')
    
    return redirect('detalle_pedido', pedido_id=pedido_id)