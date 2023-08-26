# Generated by Django 4.2 on 2023-04-19 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_project_warehouse_alter_contact_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='position',
        ),
        migrations.RemoveField(
            model_name='сancellation',
            name='position',
        ),
        migrations.AddField(
            model_name='inventory',
            name='position',
            field=models.ManyToManyField(to='store.product', verbose_name='Позиция'),
        ),
        migrations.AddField(
            model_name='сancellation',
            name='position',
            field=models.ManyToManyField(to='store.product', verbose_name='Позиция'),
        ),
    ]
