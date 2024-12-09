from datetime import datetime
from decimal import Decimal
from tabnanny import verbose
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator  # Añade esta importación
from django.db.models import Q, Sum, F  # Añadimos Sum y F a las importaciones
from django.db.models.signals import pre_save
from django.dispatch import receiver
# import ipaddress
from ipware import get_client_ip
import logging

logger = logging.getLogger(__name__)

class Tipo(models.Model):
    nombre = models.CharField(max_length=50,verbose_name='Tipo de Repuesto')
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        db_table = 'tipo'
        verbose_name = 'Tipo de Repuesto'
        verbose_name_plural = 'Tipos de Repuestos'
        ordering = ['nombre']

        # Índices para optimizar búsquedas
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['creado']),
        ]

        # Permisos específicos para el modelo
        permissions = [
            ("can_view_all_tipos", "Puede ver todos los tipos de repuestos"),
            ("can_create_tipos", "Puede crear tipos de repuestos"),
            ("can_edit_tipos", "Puede editar tipos de repuestos"),
            ("can_delete_tipos", "Puede eliminar tipos de repuestos"),
            ("can_manage_tipos", "Puede gestionar completamente los tipos"),
            ("can_export_tipos", "Puede exportar tipos de repuestos"),
        ]

        # Constraints para garantizar integridad
        constraints = [
            # Asegurar nombres únicos
            models.UniqueConstraint(
                fields=['nombre'],
                name='unique_tipo_nombre'
            ),
        ]

# En models.py, clase Repuesto, añadir un manager para filtrar por defecto
class RepuestoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)

class Repuesto(models.Model):
    
    objects = models.Manager()  # Manager por defecto
    activos = RepuestoManager()  # Manager personalizado
    
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
        ],
        editable=False  # Esto previene la edición en el admin de Django
    )
    
    activo = models.BooleanField(default=True)  # Nuevo campo

    creado = models.DateTimeField(auto_now=True,editable=False)
    
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

        # Índices para optimizar búsquedas frecuentes
        indexes = [
            models.Index(fields=['codigoRepuesto']),
            models.Index(fields=['nombre']),
            # Índice compuesto para búsquedas comunes
            models.Index(fields=['activo', 'stock'], name='repuesto_search_idx'),
        ]

        # Permisos detallados para el modelo
        permissions = [
            # Permisos de visualización
            ("can_view_all_repuestos", "Puede ver todos los repuestos"),
            ("can_view_stock", "Puede ver el stock de repuestos"),
            ("can_view_prices", "Puede ver los precios"),
            
            # Permisos de gestión básica
            ("can_create_repuestos", "Puede crear repuestos"),
            ("can_edit_repuestos", "Puede editar repuestos"),
            ("can_delete_repuestos", "Puede eliminar repuestos"),
            
            # Permisos de gestión avanzada
            ("can_manage_stock", "Puede gestionar el stock"),
            ("can_modify_prices", "Puede modificar precios"),
            ("can_activate_repuestos", "Puede activar/desactivar repuestos"),
            ("can_manage_images", "Puede gestionar imágenes de repuestos"),
            
            # Permisos de reportes y exportación
            ("can_export_repuestos", "Puede exportar repuestos"),
            ("can_view_reports", "Puede ver reportes de repuestos"),
            ("can_view_stock_history", "Puede ver historial de stock"),
        ]

        # Constraints para garantizar integridad de datos
        constraints = [
            # Asegurar código único
            models.UniqueConstraint(
                fields=['codigoRepuesto'],
                name='unique_repuesto_codigo'
            ),
            # Asegurar precio positivo
            models.CheckConstraint(
                check=models.Q(precio__gt=0),
                name='positive_precio_repuesto'
            ),
            # Asegurar stock no negativo
            models.CheckConstraint(
                check=models.Q(stock__gte=0),
                name='non_negative_stock'
            ),
        ]

# NOTE SIGNAL - Previene modificaciones no autorizadas de otras entidades
# que modifiquen Modelo.stock
# Requieren declaración explícita de self.repuesto._stock_operation = True
@receiver(pre_save, sender=Repuesto)
def prevent_stock_modification(sender, instance, **kwargs):
    """Prevenir modificaciones directas al stock"""
    if instance.pk:  # Si el objeto ya existe (es una actualización)
        original = Repuesto.objects.get(pk=instance.pk)
        if original.stock != instance.stock:
            # Si el cambio no viene de una operación de stock autorizada
            if not getattr(instance, '_stock_operation', False):
                instance.stock = original.stock  # Revertir el cambio de stock

class StockOperation(models.Model):
    OPERATION_TYPES = [
        ('INGRESO', 'Ingreso de existencias'),
        ('MERMA', 'Registro de merma'),
        ('PEDIDO', 'Asignación a pedido'),
        ('RESTITUCION', 'Restitución de pedido')
    ]

    repuesto = models.ForeignKey('Repuesto', on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message="La cantidad debe ser mayor a 0")]
    )
    tipo_operacion = models.CharField(
        max_length=30,  # Aumentamos el tamaño para acomodar 'RESTITUCION'
        choices=OPERATION_TYPES
    )
    motivo = models.TextField()
    documento_referencia = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Número de documento asociado (ej: factura, guía de despacho)"
    )
    fecha_operacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    ip_address = models.GenericIPAddressField()
    
    # def clean(self):
    #     if self.tipo_operacion == 'MERMA':
    #         if self.cantidad > self.repuesto.stock:
    #             raise ValidationError(
    #                 f"No puede registrar una merma mayor al stock disponible ({self.repuesto.stock})"
    #             )
    
    def clean(self):
        if self.tipo_operacion == 'MERMA':
            
            if not self.repuesto.activo:
                raise ValidationError("No se pueden registrar mermas de repuestos inactivos")
            if self.cantidad > self.repuesto.stock:
                raise ValidationError({
                    '__all__': f'No puede registrar una merma mayor al stock disponible ({self.repuesto.stock} unidades)'
                })
            # raise ValidationError(f"No puede registrar una merma mayor al stock disponible ({self.repuesto.stock})")
            # if self.tipo_operacion == 'MERMA' and self.cantidad > self.repuesto.stock:

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
        logger.info(f"[INSIDE StockOperation.save] Item ID: {self.id}, Cantidad: {self.cantidad}, Stock actual: {self.repuesto.stock}")
        
        self.repuesto._stock_operation = True
        # Actualizar stock del repuesto
        if self.tipo_operacion == 'INGRESO' or self.tipo_operacion == 'RESTITUCION':
            self.repuesto.stock += self.cantidad
        else:  # MERMA
            self.repuesto.stock -= self.cantidad
        self.repuesto.save()
        
    @classmethod
    def buscar(cls, query=None, tipo_operacion=None, fecha_desde=None, fecha_hasta=None):
        queryset = cls.objects.all()

        if query:
            queryset = queryset.filter(
                Q(repuesto__nombre__icontains=query) |
                Q(repuesto__codigoRepuesto__icontains=query) |
                Q(motivo__icontains=query)
            )

        if tipo_operacion:
            queryset = queryset.filter(tipo_operacion=tipo_operacion)

        if fecha_desde:
            queryset = queryset.filter(fecha_operacion__date__gte=fecha_desde)

        if fecha_hasta:
            queryset = queryset.filter(fecha_operacion__date__lte=fecha_hasta)

        return queryset.select_related('repuesto', 'usuario').order_by('-fecha_operacion')

    class Meta:
        ordering = ['-fecha_operacion']
        verbose_name = "Operación de Stock"
        verbose_name_plural = "Operaciones de Stock"
        
    def __str__(self):
        return f"{self.tipo_operacion} - {self.repuesto.nombre} ({self.cantidad})"
  
        
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
    
    # @classmethod
    def cancelar_pedido(self, usuario, ip_address):
        """Cancela el pedido y restituye el stock"""
        if self.estado == 'CANCELADO':
            return
            
        # Restituir stock de cada item
        for item in self.items.all():
            # Operacion de actualizacion stock dentro de stockoperation
            StockOperation.objects.create(
                repuesto=item.repuesto,
                cantidad=item.cantidad,
                tipo_operacion='RESTITUCION',
                motivo=f'Cancelación de pedido #{self.id}',
                usuario=usuario,
                ip_address=ip_address
            )
            
            print("item cantidad ${item.cantidad}")
        
        self.estado = 'CANCELADO'
        self.save()



    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"
    
    class Meta:
        db_table = 'tiendaApp_pedido'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_creacion']  # Ordenar por fecha de creación, más reciente primero
        
        # Índices para mejorar el rendimiento de las búsquedas
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_creacion']),
            models.Index(fields=['cliente']),
        ]
        
        # Permisos específicos para el modelo
        permissions = [
            ("can_view_all_pedidos", "Puede ver todos los pedidos"),
            ("can_create_pedidos", "Puede crear pedidos"),
            ("can_edit_pedidos", "Puede editar pedidos"),
            ("can_delete_pedidos", "Puede eliminar pedidos"),
            ("can_cancel_pedidos", "Puede cancelar pedidos"),
            ("can_confirm_pedidos", "Puede confirmar pedidos"),
            ("can_mark_as_delivered", "Puede marcar pedidos como entregados"),
            ("can_view_pedidos_reports", "Puede ver reportes de pedidos"),
            ("can_export_pedidos", "Puede exportar pedidos"),
            ("can_manage_own_pedidos", "Puede gestionar sus propios pedidos"),
        ]
        
        # Constraints para garantizar integridad de datos
        constraints = [
            models.CheckConstraint(
                check=models.Q(estado__in=[
                    'PENDIENTE', 'CONFIRMADO', 'ENTREGADO', 'CANCELADO'
                ]),
                name='valid_estado_pedido'
            )
        ]
    
class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    repuesto = models.ForeignKey('Repuesto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message="La cantidad debe ser mayor a 0")]
    )
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        
        if not self.precio_unitario:
            self.precio_unitario = self.repuesto.precio
        
        if self._state.adding:  # Si es una nueva instancia
            if self.pedido.estado == 'CANCELADO':
                raise ValidationError("No se pueden agregar items a un pedido cancelado")
               
               
            # Crear operación de stock tipo PEDIDO
            ip_address = '0.0.0.0'
            if request:
                client_ip, _ = get_client_ip(request)
                ip_address = client_ip or '0.0.0.0'
                 
            # Crear operación de stock tipo PEDIDO
            # Actualiza stock - no es necesario ingresar nueva cantidad
            StockOperation.objects.create(
                repuesto=self.repuesto,
                cantidad=self.cantidad,
                tipo_operacion='PEDIDO',
                motivo=f'Asignación a pedido #{self.pedido.id}',
                usuario=self.pedido.creado_por,
                ip_address=ip_address
            )
            
            # Actualizar stock
            # nuevo_stock = self.repuesto.stock - self.cantidad
            
            # self.repuesto.stock -= self.cantidad
            # self.repuesto._stock_operation = True  
            
            # self.repuesto.save()
            
            
        super().save(*args, **kwargs)
        
        
    def delete(self, *args, **kwargs):
        if self.pedido.estado == 'CANCELADO':
            raise ValidationError("No se pueden eliminar items de un pedido cancelado")
            
        # Restaurar stock solo si el pedido no está cancelado
        # if self.pedido.estado != 'CANCELADO':
        #     self.repuesto.stock += self.cantidad
        #     self.repuesto.save()
            
        # Restaurar stock y registrar operación solo si el pedido no está cancelado
        if self.pedido.estado != 'CANCELADO':
            request = kwargs.pop('request', None)

            ip_address = '0.0.0.0'
            if request:
                client_ip, _ = get_client_ip(request)
                ip_address = client_ip or '0.0.0.0'
                
            logger.info(f"[BEFORE] Item ID: {self.id}, Cantidad: {self.cantidad}, Stock actual: {self.repuesto.stock}")

            # Crear operación de stock tipo RESTITUCION
            StockOperation.objects.create(
                repuesto=self.repuesto,
                cantidad=self.cantidad,
                tipo_operacion='RESTITUCION',
                motivo=f'Eliminación de item en pedido #{self.pedido.id}',
                usuario=self.pedido.creado_por,
                ip_address=ip_address,
                documento_referencia=''
            )
            
            logger.info(f"[BEFORE-CHUINK] Item ID: {self.id}, Cantidad: {self.cantidad}, Stock actual: {self.repuesto.stock}")
            
            # Restaurar stock
            # self.repuesto.stock += self.cantidad
            # self.repuesto._stock_operation = True
            
            logger.info(f"[AFTER] Item ID: {self.id}, Cantidad: {self.cantidad}, Stock actual: {self.repuesto.stock}")
            

            self.repuesto.save()
        
        super().delete(*args, **kwargs)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.repuesto.nombre} x {self.cantidad}"
    
    class Meta:
        db_table = 'tiendaApp_pedidoitem'
        verbose_name = 'Item de Pedido'
        verbose_name_plural = 'Items de Pedido'
        ordering = ['pedido', 'repuesto__nombre']  # Ordenar por pedido y nombre de repuesto
        
        # Índices optimizados
        indexes = [
            # Índice compuesto para la consulta más común:
            # Buscar items por pedido y repuesto
            models.Index(
                fields=['pedido', 'repuesto'],
                name='pedido_repuesto_idx'
            ),
        ]
        
        # Permisos específicos para el modelo
        permissions = [
            ("can_view_all_items", "Puede ver todos los items de pedidos"),
            ("can_add_items", "Puede añadir items a pedidos"),
            ("can_modify_items", "Puede modificar items de pedidos"),
            ("can_delete_items", "Puede eliminar items de pedidos"),
            ("can_modify_prices", "Puede modificar precios de items"),
            ("can_view_item_history", "Puede ver historial de items"),
        ]
        
        # Constraints para garantizar integridad de datos
        constraints = [
            models.CheckConstraint(
                check=models.Q(cantidad__gt=0),
                name='positive_cantidad'
            ),
            models.CheckConstraint(
                check=models.Q(precio_unitario__gt=0),
                name='positive_precio'
            ),
            # Evitar duplicados de repuesto en el mismo pedido
            models.UniqueConstraint(
                fields=['pedido', 'repuesto'],
                name='unique_repuesto_per_pedido'
            )
        ]