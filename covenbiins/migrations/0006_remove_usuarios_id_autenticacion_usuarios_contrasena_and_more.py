# Generated by Django 4.2.7 on 2024-01-30 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covenbiins', '0005_usuarios_foto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuarios',
            name='id_Autenticacion',
        ),
        migrations.AddField(
            model_name='usuarios',
            name='contrasena',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='usuarios',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
    ]
