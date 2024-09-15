# Generated by Django 4.2.9 on 2024-09-15 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_message_receiver_seen_alter_customer_timestamp_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prices',
            name='timestamp_status',
        ),
        migrations.AddField(
            model_name='prices',
            name='cooldown_end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='timestamp',
            field=models.IntegerField(default=1726431859.8175774),
        ),
        migrations.AlterField(
            model_name='prices',
            name='timestamp',
            field=models.IntegerField(default=1726431861.6583135),
        ),
        migrations.AlterField(
            model_name='products',
            name='timestamp',
            field=models.IntegerField(default=1726431859.8185778),
        ),
        migrations.AlterField(
            model_name='rating',
            name='timestamp',
            field=models.IntegerField(default=1726431861.6603148),
        ),
    ]
