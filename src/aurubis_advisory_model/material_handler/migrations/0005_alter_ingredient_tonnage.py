# Generated by Django 4.2.6 on 2023-10-11 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material_handler', '0004_alter_measurement_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='tonnage',
            field=models.IntegerField(),
        ),
    ]
