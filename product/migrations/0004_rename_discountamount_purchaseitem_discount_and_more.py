# Generated by Django 5.1.2 on 2024-11-29 19:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_purchaseitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchaseitem',
            old_name='discountAmount',
            new_name='discount',
        ),
        migrations.RenameField(
            model_name='purchaseitem',
            old_name='total_amount',
            new_name='totalAmount',
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='productname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_items', to='product.product'),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_items', to='product.purchase'),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
