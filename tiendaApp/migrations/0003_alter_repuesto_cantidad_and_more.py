# Generated by Django 4.1 on 2024-12-01 16:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import tiendaApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendaApp', '0002_alter_pedidoitem_cantidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repuesto',
            name='cantidad',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='tiendaApp.cantidad'),
        ),
        migrations.AlterField(
            model_name='repuesto',
            name='codigoRepuesto',
            field=models.CharField(editable=False, max_length=20, verbose_name='Código del Repuesto'),
        ),
        migrations.AlterField(
            model_name='repuesto',
            name='fotografia',
            field=models.ImageField(blank=True, default='repuestos/tractor.png', null=True, upload_to=tiendaApp.models.Repuesto.imagen_path),
        ),
        migrations.AlterField(
            model_name='repuesto',
            name='nombre',
            field=models.CharField(max_length=160, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='repuesto',
            name='precio',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='El precio debe ser mayor a 0'), django.core.validators.MaxValueValidator(99999999, message='El precio es demasiado alto')], verbose_name='Precio'),
        ),
    ]
