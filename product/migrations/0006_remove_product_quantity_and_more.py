# Generated by Django 5.1.2 on 2024-11-09 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='product',
            name='reorder_quantity',
        ),
    ]