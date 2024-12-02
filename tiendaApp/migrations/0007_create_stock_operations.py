# tiendaApp/migrations/0007_stockoperation.py

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tiendaApp', '0006_remove_repuesto_cantidad_repuesto_stock_and_more'),  # Asegúrate de poner aquí la migración anterior correcta
    ]

    operations = [
        migrations.CreateModel(
            name='StockOperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('tipo_operacion', models.CharField(choices=[('INGRESO', 'Ingreso de existencias'), ('MERMA', 'Registro de merma'), ('PEDIDO', 'Asignación a pedido'), ('RESTITUCION', 'Restitución de pedido')], max_length=20)),
                ('motivo', models.TextField()),
                ('fecha_operacion', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('repuesto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tiendaApp.repuesto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Operación de Stock',
                'verbose_name_plural': 'Operaciones de Stock',
                'ordering': ['-fecha_operacion'],
            },
        ),
    ]