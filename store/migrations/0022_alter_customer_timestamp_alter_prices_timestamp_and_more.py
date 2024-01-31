# Generated by Django 4.2.9 on 2024-01-31 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_customer_timestamp_rating_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='timestamp',
            field=models.IntegerField(default=1706709791.7669914),
        ),
        migrations.AlterField(
            model_name='prices',
            name='timestamp',
            field=models.IntegerField(default=1706709791.7812521),
        ),
        migrations.AlterField(
            model_name='prices',
            name='timestamp_status',
            field=models.IntegerField(blank=True, default=1706709791.7812521, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='timestamp',
            field=models.IntegerField(default=1706709791.7669914),
        ),
        migrations.AlterField(
            model_name='rating',
            name='timestamp',
            field=models.IntegerField(default=1706709791.7832792),
        ),
    ]
