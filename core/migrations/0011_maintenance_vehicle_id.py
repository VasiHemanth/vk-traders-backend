# Generated by Django 4.2.7 on 2024-01-17 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_vehicle_id_alter_vehicle_registration_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenance',
            name='vehicle_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='core.vehicle'),
            preserve_default=False,
        ),
    ]
