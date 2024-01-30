# Generated by Django 4.2.9 on 2024-01-30 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_remove_prices_date_offer_prices_timestamp_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prices',
            name='date_status',
        ),
        migrations.AddField(
            model_name='prices',
            name='timestamp_status',
            field=models.IntegerField(blank=True, default=1706628195.4810116, null=True),
        ),
        migrations.AlterField(
            model_name='prices',
            name='timestamp',
            field=models.IntegerField(default=1706628195.4810116),
        ),
        migrations.AlterField(
            model_name='products',
            name='timestamp',
            field=models.IntegerField(default=1706628195.462063),
        ),
    ]
