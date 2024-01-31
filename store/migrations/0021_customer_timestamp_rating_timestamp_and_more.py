# Generated by Django 4.2.9 on 2024-01-30 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_products_listed_alter_prices_timestamp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='timestamp',
            field=models.IntegerField(default=1706637284.275803),
        ),
        migrations.AddField(
            model_name='rating',
            name='timestamp',
            field=models.IntegerField(default=1706637284.3086872),
        ),
        migrations.AlterField(
            model_name='prices',
            name='timestamp',
            field=models.IntegerField(default=1706637284.2957222),
        ),
        migrations.AlterField(
            model_name='prices',
            name='timestamp_status',
            field=models.IntegerField(blank=True, default=1706637284.2957222, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='timestamp',
            field=models.IntegerField(default=1706637284.275803),
        ),
    ]