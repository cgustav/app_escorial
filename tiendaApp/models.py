from datetime import datetime
from decimal import Decimal
from tabnanny import verbose
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator  # Añade esta importación
from django.db.models import Q, Sum, F  # Añadimos Sum y F a las importaciones

import os

# Create your models here.



class Tipo(models.Model):
    nombre = models.CharField(max_length=50,verbose_name='Tipo de Repuesto')
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        db_table = 'tipo'
        verbose_name = 'tipo'
        verbose_name_plural = 'Tipos'

# NOTE DEPRECATE CLASS!!
# class Cantidad(models.Model):
#     nombre = models.CharField(max_length=50,verbose_name='Stock del repuesto ')
#     creado = models.DateTimeField(default=timezone.now)

#     def get_valor_numerico(self):
#             try:
#                 # Intenta convertir el nombre (que contiene el stock) a entero
#                 return int(self.nombre)
#             except ValueError:
#                 return 0
        
#     def __str__(self):
#         return "{}".format(self.nombre)

#     class Meta:
#         db_table = 'cantidad'
#         verbose_name = 'Cantidad'
#         verbose_name_plural = 'Cantidades'

class Repuesto(models.Model):
    codigoRepuesto = models.CharField(max_length=20,verbose_name='Código del Repuesto', editable=False)
    nombre = models.CharField(max_length=160,verbose_name='Nombre')
    tipo = models.ForeignKey(Tipo,null=False,on_delete=models.RESTRICT)
    # precio = models.PositiveIntegerField(default=8000,null=False, verbose_name='Precio')
    precio = models.PositiveIntegerField(
        verbose_name='Precio',
        validators=[
            MinValueValidator(1, message="El precio debe ser mayor a 0"),
            MaxValueValidator(99999999, message="El precio excede lo permitido")
        ]
    )
    
    # NOTE REFACTOR CANTIDADES - READY TO REVIEW
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name='Stock disponible',
        validators=[
            MinValueValidator(0, message="El stock no puede ser negativo")
        ]
    )
    
    # TODO CLEAN THIS AFTER VALIDATE REFACTOR
    # cantidad = models.ForeignKey('Cantidad', on_delete=models.CASCADE)  # asumiendo que este es tu modelo
    # cantidad = models.ForeignKey(
    #     'Cantidad',
    #     on_delete=models.CASCADE,
    #     null=True,  # Mantenemos null=True
    #     default=None  # Valor por defecto None
    # )
    
    
    creado = models.DateTimeField(auto_now=True,editable=False)

    # NOTE: Metodo anterior
    # def generarNombre(instance, filename):
    #     extension = os.path.splittext(filename)[1][1:]  # Obtener la extensión del archivo
    #     ruta = 'empleados'
    #     fecha = timezone.now().strftime('%Y%m%d_%H%M%S')  # Agregar marca de tiempo
    #     nombre = "{}.{}".format(fecha,extension)
    #     return os.path.join(ruta,nombre)
    
    # Genera una ruta unica para imagenes /(BucketS3)
    def imagen_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = f"{instance.codigoRepuesto}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
        return f'repuestos/{filename}'
    
    fotografia = models.ImageField(
        upload_to=imagen_path, 
        null=True, 
        blank=True, 
        default='repuestos/tractor.png'
    )
    
    # @property
    # def stock_disponible(self):
    #     return getattr(self.cantidad, 'valor', self.cantidad)
    
    
    def get_valor_numerico(self):
        return self.stock

    def save(self, *args, **kwargs):
        
        if not self.codigoRepuesto:
            # Generar código automático
            ultimo_repuesto = Repuesto.objects.order_by('-codigoRepuesto').first()
            if ultimo_repuesto:
                ultimo_numero = int(ultimo_repuesto.codigoRepuesto[3:])
                nuevo_numero = ultimo_numero + 1
            else:
                nuevo_numero = 1
            self.codigoRepuesto = f'REP{nuevo_numero:04d}'
            
        # Verificar si la imagen ya está configurada
        if not self.fotografia:
            self.fotografia = 'repuestos/tractor.png'  # Asignar la imagen por defecto

        super().save(*args, **kwargs)
        
# METODO DE BUSQUEDA DE PRODUCTOS A TRAVÉS DE FRONTEND
    @classmethod
    def buscar(cls, query):
        if not query:
            return cls.objects.all()
        
        # Dividir la consulta en palabras para búsqueda parcial
        palabras = query.split()
        q_objects = Q()
        
        # Construir consulta para cada palabra
        for palabra in palabras:
            q_objects |= (
                Q(nombre__icontains=palabra) |
                Q(codigoRepuesto__icontains=palabra) |
                Q(tipo__nombre__icontains=palabra)
            )
            
            # Intentar convertir a número para búsqueda por precio
            try:
                precio = int(palabra)
                q_objects |= Q(precio__lte=precio + 1000) & Q(precio__gte=precio - 1000)
            except ValueError:
                pass
        
        return cls.objects.filter(q_objects).distinct()

    @classmethod
    def aplicar_filtros(cls, queryset, tipo=None, orden=None):
        """
        Aplica filtros y ordenamiento a un queryset de Repuestos
        """
        if tipo:
            queryset = queryset.filter(tipo_id=tipo)
        
        if orden:
            if orden in ['-precio', 'precio', '-nombre', 'nombre']:
                queryset = queryset.order_by(orden)
                
        return queryset
    
    def __str__(self):
        return "{} {}".format(self.nombre, self.codigoRepuesto)

    class Meta:
        db_table = 'repuesto'
        verbose_name = 'Repuesto'
        verbose_name_plural = 'Repuestos'
        ordering = ['nombre']
        
        
class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADO', 'Confirmado'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    cliente = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    notas = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='pedidos_creados')

    def calcular_total(self):
        return sum(item.subtotal() for item in self.items.all())
    
    # Aplicacion sistema de búsqueda:
    # 
    # - Encontrar coincidencias por palabra
    @classmethod
    def buscar(cls, query):
        if not query:
            return cls.objects.all()
        
        q_objects = Q()
        
        # Buscar coincidencias exactas o parciales en los campos principales
        q_objects |= Q(cliente__icontains=query)
        q_objects |= Q(telefono__icontains=query)
        q_objects |= Q(email__icontains=query)
        
        # Buscar por ID de pedido
        try:
            id_pedido = int(query)
            q_objects |= Q(id=id_pedido)
        except ValueError:
            pass
        
        return cls.objects.filter(q_objects).distinct()
    
    # Aplicacion sistema de búsqueda:
    # 
    # - Ordenamientos y filtros por:
    #   - Estado
    #   - Fecha de creación
    #   -
    @classmethod
    def aplicar_filtros(cls, queryset, estado=None, orden=None, fecha_desde=None, fecha_hasta=None):
        """
        Aplica filtros y ordenamiento a un queryset de Pedidos
        """
        if estado:
            queryset = queryset.filter(estado=estado)
        
        if fecha_desde:
            queryset = queryset.filter(fecha_creacion__gte=fecha_desde)
        
        if fecha_hasta:
            queryset = queryset.filter(fecha_creacion__lte=fecha_hasta)
        
        if orden:
            if orden in ['fecha_asc', '-fecha_creacion', 'total_asc', 'total_desc', 'cliente']:
                if orden == 'fecha_asc':
                    queryset = queryset.order_by('fecha_creacion')
                elif orden == 'total_asc':
                    queryset = queryset.annotate(
                        total=Sum(F('items__cantidad') * F('items__precio_unitario'))
                    ).order_by('total')
                elif orden == 'total_desc':
                    queryset = queryset.annotate(
                        total=Sum(F('items__cantidad') * F('items__precio_unitario'))
                    ).order_by('-total')
                elif orden == 'cliente':
                    queryset = queryset.order_by('cliente')
                else:
                    queryset = queryset.order_by(orden)
                    
        return queryset

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"
    
class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    repuesto = models.ForeignKey('Repuesto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message="La cantidad debe ser mayor a 0")]
    )
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.precio_unitario:
            self.precio_unitario = self.repuesto.precio
        
        if self._state.adding:  # Si es una nueva instancia
            
            # NOTE: DEPRECAT - REFACTOR DE CANTIDADES
            # Convertir a entero para la comparación
            # cantidad_actual = int(self.repuesto.cantidad)
            # self.repuesto.cantidad = cantidad_actual - self.cantidad
            # self.repuesto.save()
            # stock_actual = self.repuesto.cantidad.get_valor_numerico()
            # nuevo_stock = str(stock_actual - self.cantidad)
            # self.repuesto.cantidad.nombre = nuevo_stock
            
            # TODO REVIEW THIS - CANTIDADES CHANGES TO STOCK
            if self.cantidad > self.repuesto.stock:
                raise ValidationError(f"No hay suficiente stock. Disponible: {self.repuesto.stock}")
            self.repuesto.stock -= self.cantidad
            
            self.repuesto.cantidad.save()
            
        super().save(*args, **kwargs)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.repuesto.nombre} x {self.cantidad}"