from dataclasses import fields
# from socket import fromshare
# from tkinter.tix import Select
from django import forms
from tiendaApp.models import Tipo,Repuesto, Pedido, PedidoItem, StockOperation
from django.core.exceptions import ValidationError

import datetime


class RepuestoForm(forms.ModelForm):
    # codigoRepuesto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Ingrese código repuesto'}))
    
    codigoRepuesto = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
            'placeholder': 'Se generará automáticamente'
        }),
        required=False
    )
    # nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Ingrese nombre'}))
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese nombre'
        }),
        max_length=160
    )
    # precio = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Ingrese precio'}))
    
    precio = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese precio',
            'min': '1',
            'max': '99999999'
        }),
        min_value=1,
        max_value=99999999
    )
    
    # NOTE Metodo Antiguo
    # fotografia = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}), required=False)
    
    # NOTE Nuevo Metodo S3
    fotografia = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        error_messages={
            'invalid_image': 'El archivo debe ser una imagen válida'
        }
    )

   
    tipo = forms.ModelChoiceField(
        queryset=Tipo.objects.all().order_by('-nombre'),  # Orden descendente
        empty_label='Seleccione un tipo de repuesto',
        widget=forms.Select(attrs={'class':'form-control'})
    )
    
    # NOTE CODIGO REFACTORIZADO - REFACTOR FROM cantidad to stock
    # cantidad = forms.ModelChoiceField(
    #     queryset=Cantidad.objects.all(),
    #     empty_label='Seleccione una cantidad',
    #     widget=forms.Select(attrs={'class':'form-control'})
    # )
    
    # TODO REVIEW THIS AFTER REFACTOR FROM cantidad to stock
    stock = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
            'placeholder': 'Stock disponible',
            'min': '0',
            'max': '99999'
        }),
        min_value=0,
        max_value=99999
    )

    class Meta:
        model = Repuesto
        fields = '__all__'
        exclude =['fotografia', 'stock']
        
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None:
            if precio <= 0:
                raise ValidationError("El precio debe ser mayor a 0")
            if precio > 99999999:
                raise ValidationError("El precio es demasiado alto")
        return precio
    
    def clean_fotografia(self):
        foto = self.cleaned_data.get('fotografia')
        if foto:
            # Validar tamaño máximo (ejemplo: 8MB)
            if foto.size > 8 * 1024 * 1024:
                raise ValidationError("La imagen no debe superar los 8MB")
            
            # Validar tipos de archivo permitidos
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
            if foto.content_type not in allowed_types:
                raise ValidationError("Solo se permiten archivos JPEG y PNG")
        return foto


class SearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre, código, tipo o precio...',
            'autocomplete': 'off'
        })
    )
    tipo = forms.ModelChoiceField(
        queryset=Tipo.objects.all(),
        required=False,
        empty_label="Todos los tipos",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    orden = forms.ChoiceField(
        choices=[
            ('nombre', 'Nombre (A-Z)'),
            ('-nombre', 'Nombre (Z-A)'),
            ('precio', 'Precio (menor a mayor)'),
            ('-precio', 'Precio (mayor a menor)'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class StockOperationForm(forms.ModelForm):
    class Meta:
        model = StockOperation
        fields = ['repuesto', 'cantidad', 'motivo', 'documento_referencia']
        
    def __init__(self, *args, **kwargs):
        self.tipo_operacion = kwargs.pop('tipo_operacion', None)
        self.user = kwargs.pop('user', None)
        self.ip_address = kwargs.pop('ip_address', None)
        super().__init__(*args, **kwargs)

        # Filtrar solo repuestos activos y con stock > 0 para mermas
        if self.tipo_operacion == 'MERMA':
            self.fields['repuesto'].queryset = Repuesto.activos.filter(stock__gt=0)
        else:
            self.fields['repuesto'].queryset = Repuesto.activos.all()
            

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tipo_operacion = self.tipo_operacion
        instance.usuario = self.user
        instance.ip_address = self.ip_address
        if commit:
            instance.save()
        return instance
    
    
class StockOperationSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por repuesto o motivo...'
        })
    )
    tipo_operacion = forms.ChoiceField(
        choices=[('', 'Todos los tipos')] + StockOperation.OPERATION_TYPES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'telefono', 'email', 'notas']
        widgets = {
            'notas': forms.Textarea(attrs={'rows': 3}),
        }
        
        
class PedidoSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por cliente, teléfono o N° de pedido...',
            'autocomplete': 'off'
        })
    )
    estado = forms.ChoiceField(
        choices=[('', 'Todos los estados')] + Pedido.ESTADO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    orden = forms.ChoiceField(
        choices=[
            ('-fecha_creacion', 'Más recientes primero'),
            ('fecha_asc', 'Más antiguos primero'),
            ('cliente', 'Cliente (A-Z)'),
            ('total_asc', 'Total (menor a mayor)'),
            ('total_desc', 'Total (mayor a menor)'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class PedidoItemForm(forms.ModelForm):
    class Meta:
        model = PedidoItem
        fields = ['repuesto', 'cantidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={
                'min': '1',
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo repuestos con stock disponible
        self.fields['repuesto'].queryset = Repuesto.objects.filter(
            activo=True,
            stock__gt=0
        )
        self.fields['repuesto'].widget.attrs.update({'class': 'form-select'})

    def clean(self):
        cleaned_data = super().clean()
        repuesto = cleaned_data.get('repuesto')
        cantidad = cleaned_data.get('cantidad')

        if repuesto and cantidad:
            # Obtener el valor numérico de la cantidad del repuesto
            # stock_disponible = getattr(repuesto.cantidad, 'valor', repuesto.cantidad)
            stock_disponible = repuesto.stock

            if cantidad <= 0:
                raise ValidationError("La cantidad debe ser mayor a 0")
                
            if cantidad > stock_disponible:
                raise ValidationError(f"Solo hay {stock_disponible} unidades disponibles de {repuesto.nombre}")
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not hasattr(instance, 'precio_unitario') or not instance.precio_unitario:
            instance.precio_unitario = instance.repuesto.precio
        if commit:
            # Actualizar el stock del repuesto
            # stock_actual = getattr(instance.repuesto.cantidad, 'valor', instance.repuesto.cantidad)
            stock_actual = instance.repuesto.cantidad.get_valor_numerico()

            nuevo_stock = str(stock_actual - instance.cantidad)
            instance.repuesto.cantidad.nombre = nuevo_stock
            instance.repuesto.cantidad.save()
            instance.save()
        return instance