# Generated by Django 4.2.4 on 2024-01-16 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_customer_register_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_banned',
            field=models.BooleanField(default=False),
        ),
    ]
