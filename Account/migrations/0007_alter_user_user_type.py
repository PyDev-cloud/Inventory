# Generated by Django 5.1.2 on 2024-11-09 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0006_alter_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('Employee', 'Employee'), ('Admin', 'Admin'), ('Staff', 'Staff')], default='Staff', max_length=30),
        ),
    ]
