# Generated by Django 4.2.7 on 2024-02-19 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covenbiins', '0012_alter_inmuebles_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmuebles',
            name='imagen',
            field=models.ImageField(default='fotos_inmuebles/default.png', upload_to='fotos_inmuebles'),
        ),
    ]
