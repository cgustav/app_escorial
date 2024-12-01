from django.db import migrations, models
from django.core.validators import MinValueValidator

def transferir_cantidades(apps, schema_editor):
    Repuesto = apps.get_model('tiendaApp', 'Repuesto')
    for repuesto in Repuesto.objects.all():
        if repuesto.cantidad:
            try:
                repuesto.stock = int(repuesto.cantidad.nombre)
            except (ValueError, AttributeError):
                repuesto.stock = 0
            repuesto.save()

def revertir_cambios(apps, schema_editor):
    pass  # No es necesario implementar la reversión ya que eliminaremos el modelo Cantidad

class Migration(migrations.Migration):
    dependencies = [
        ('tiendaApp', '0003_alter_repuesto_cantidad_and_more'),  # Ajusta este nombre según tu última migración
    ]

    operations = [
        # Añadir el nuevo campo stock
        migrations.AddField(
            model_name='repuesto',
            name='stock',
            field=models.PositiveIntegerField(
                default=0, 
                verbose_name='Stock disponible',
                validators=[MinValueValidator(0, message="El stock no puede ser negativo")]
            ),
        ),
        # Ejecutar la función de transferencia
        migrations.RunPython(transferir_cantidades, revertir_cambios),
        # Eliminar la relación con Cantidad
        migrations.RemoveField(
            model_name='repuesto',
            name='cantidad',
        ),
        # Eliminar el modelo Cantidad
        migrations.DeleteModel(
            name='Cantidad',
        ),
    ]