# Generated by Django 5.1.2 on 2024-12-06 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_rename_totalamount_purchaseitem_product_totalamount'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellesInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=100, unique=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('paid_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('GrandTotal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('dueAmount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
    ]
