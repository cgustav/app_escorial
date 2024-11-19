from dataclasses import fields
# from socket import fromshare
# from tkinter.tix import Select
from django import forms
from tiendaApp.models import Tipo,Cantidad,Repuesto, Pedido, PedidoItem
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
    
    fotografia = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}), required=False)
   
    tipo = forms.ModelChoiceField(
        queryset=Tipo.objects.all().order_by('-nombre'),  # Orden descendente
        empty_label='Seleccione un tipo de repuesto',
        widget=forms.Select(attrs={'class':'form-control'})
    )
    cantidad = forms.ModelChoiceField(
        queryset=Cantidad.objects.all(),
        empty_label='Seleccione una cantidad',
        widget=forms.Select(attrs={'class':'form-control'})
    )

    class Meta:
        model = Repuesto
        fields = '__all__'
        exclude =['fotografia']
        
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None:
            if precio <= 0:
                raise ValidationError("El precio debe ser mayor a 0")
            if precio > 99999999:
                raise ValidationError("El precio es demasiado alto")
        return precio

class SearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar insumo...'
        })
    )
    # query = forms.CharField(label='Buscar', max_length=100)


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'telefono', 'email', 'notas']
        widgets = {
            'notas': forms.Textarea(attrs={'rows': 3}),
        }

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
        self.fields['repuesto'].queryset = self.fields['repuesto'].queryset.filter(cantidad__gt=0)
        self.fields['repuesto'].widget.attrs.update({'class': 'form-select'})

    def clean(self):
        cleaned_data = super().clean()
        repuesto = cleaned_data.get('repuesto')
        cantidad = cleaned_data.get('cantidad')

        if repuesto and cantidad:
            # Obtener el valor numérico de la cantidad del repuesto
            # stock_disponible = getattr(repuesto.cantidad, 'valor', repuesto.cantidad)
            stock_disponible = repuesto.cantidad.get_valor_numerico()

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