# Generated by Django 5.2.1 on 2025-06-17 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('codigo_municipio', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre_municipio', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id_rol', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_rol', models.CharField(max_length=50)),
            ],
        ),
    ]
