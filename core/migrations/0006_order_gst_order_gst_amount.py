# Generated by Django 4.2.7 on 2024-01-14 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_trip_maintanance_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='gst',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='gst_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
