# Generated by Django 5.1.2 on 2024-12-01 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0007_alter_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('Staff', 'Staff'), ('Employee', 'Employee'), ('Admin', 'Admin')], default='Staff', max_length=30),
        ),
    ]
