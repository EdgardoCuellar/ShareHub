# Generated by Django 4.2.9 on 2024-01-30 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_remove_prices_date_status_prices_timestamp_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='listed',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='prices',
            name='timestamp',
            field=models.IntegerField(default=1706636332.4700916),
        ),
        migrations.AlterField(
            model_name='prices',
            name='timestamp_status',
            field=models.IntegerField(blank=True, default=1706636332.4700916, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='timestamp',
            field=models.IntegerField(default=1706636332.4571574),
        ),
    ]
