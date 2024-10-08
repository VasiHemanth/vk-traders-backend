# Generated by Django 4.2.7 on 2023-12-28 05:27

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.TextField(unique=True)),
                ('password', models.TextField()),
                ('name', models.TextField()),
                ('role', models.TextField()),
            ],
            options={
                'db_table': 'app_users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('driver_name', models.CharField(unique=True)),
                ('active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'driver',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('grade', models.CharField()),
                ('quantity', models.FloatField()),
                ('from_field', models.CharField(db_column='from')),
                ('to', models.CharField()),
                ('order_id', models.CharField()),
                ('party_name', models.CharField()),
                ('advance', models.CharField()),
                ('loading', models.IntegerField(blank=True, null=True)),
                ('unloading', models.IntegerField(blank=True, null=True)),
                ('rto_pcl', models.IntegerField(blank=True, null=True)),
                ('toll_gate', models.IntegerField(blank=True, null=True)),
                ('total_expenses', models.IntegerField(blank=True, null=True)),
                ('freight', models.IntegerField(blank=True, null=True)),
                ('freight_amount', models.IntegerField(blank=True, null=True)),
                ('driver_freight', models.IntegerField(blank=True, null=True)),
                ('driver_amount', models.IntegerField(blank=True, null=True)),
                ('order_submit_status', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'db_table': 'order',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrderToTripMapping',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order_id', models.TextField()),
                ('trip_id', models.TextField()),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'order_to_trip_mapping',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('trip_date', models.DateTimeField()),
                ('diesel', models.FloatField(blank=True, null=True)),
                ('trip_type', models.CharField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('vehicle_id', models.CharField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reading', models.IntegerField(blank=True, null=True)),
                ('diesel_amount', models.FloatField(blank=True, null=True)),
                ('ad_blue', models.FloatField(blank=True, null=True)),
                ('kilometers', models.IntegerField(blank=True, null=True)),
                ('no_of_trips', models.SmallIntegerField()),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('owner_name', models.CharField()),
                ('mileage', models.FloatField(blank=True, null=True)),
                ('submit_status', models.BooleanField(default=False)),
                ('balance_amount', models.FloatField(blank=True, null=True)),
                ('diesel_per_litre', models.FloatField(blank=True, null=True)),
                ('maintanance', models.FloatField(default=0)),
            ],
            options={
                'db_table': 'trip',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('registration_number', models.CharField()),
                ('company', models.CharField()),
                ('chassis_number', models.CharField(blank=True, null=True)),
                ('insurance', models.DateField(blank=True, null=True)),
                ('fc', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('driver_name', models.CharField(blank=True, null=True)),
                ('rc', models.DateField(blank=True, db_comment='RC expire date', null=True)),
            ],
            options={
                'db_table': 'vehicle',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.role')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.authuser')),
            ],
        ),
    ]
