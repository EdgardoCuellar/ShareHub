# Generated by Django 4.2.4 on 2024-01-16 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_forgotpassword'),
    ]

    operations = [
        migrations.AddField(
            model_name='prices',
            name='date_offer',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='prices',
            name='date_status',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='prices',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='prices',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
