from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from tiendaApp.forms import RepuestoForm, SearchForm, PedidoForm, PedidoItemForm
from django.contrib import messages
from tiendaApp.models import Repuesto,Tipo,Cantidad, Pedido, PedidoItem
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
    repuestos = Repuesto.objects.all()
    paginator = Paginator(repuestos, 10)  # 10 items por página
    tipos = Tipo.objects.all()
    cantidades = Cantidad.objects.all()
    
    # Paginador de repuestos
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Código de búsqueda
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            repuestos = Repuesto.objects.filter(nombre__icontains=query)
    else:
        form = SearchForm()

    data = {
        'page_obj': page_obj,
        'repuestos': repuestos,
        'tipos': tipos,
        'cantidades': cantidades,
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
            if 'fotografia' in request.FILES:
                repuesto.fotografia = request.FILES['fotografia']
            form.save()
            return redirect('repuestos')
    else:
        form = RepuestoForm(instance=repuesto)

    return render(request, 'tiendaTemplates/repuestos.html', {'form':form})

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
    pedidos = Pedido.objects.all().order_by('-fecha_creacion')
    return render(request, 'pedidos/lista_pedidos.html', {
        'pedidos': pedidos
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