# Generated by Django 5.1.2 on 2024-12-02 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_purchaseinvoice_grandtotal_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='selles',
            old_name='totalPrice',
            new_name='totalAmount',
        ),
    ]