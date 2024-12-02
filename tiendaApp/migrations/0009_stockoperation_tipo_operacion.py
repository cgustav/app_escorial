# tiendaApp/migrations/XXXX_alter_stockoperation_tipo_operacion.py
from django.db import migrations, models

class Migration(migrations.Migration):

   dependencies = [
       ('tiendaApp', '0008_alter_repuesto_stock_and_more'),  # Reemplaza con tu migración anterior
   ]

   operations = [
       migrations.AlterField(
           model_name='stockoperation',
           name='tipo_operacion',
           field=models.CharField(
               choices=[
                   ('INGRESO', 'Ingreso de existencias'),
                   ('MERMA', 'Registro de merma'),
                   ('PEDIDO', 'Asignación a pedido'),
                   ('RESTITUCION', 'Restitución de pedido')
               ],
               max_length=20,
           ),
       ),
   ]