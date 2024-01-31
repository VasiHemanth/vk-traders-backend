# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class AppUsers(models.Model):
    email = models.TextField(unique=True)
    password = models.TextField()
    name = models.TextField()
    role = models.TextField()

    class Meta:
        managed = False
        db_table = 'app_users'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()


    def __str__(self) -> str:
        return self.username

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.CharField(unique=True)

    def __str__(self) -> str:
        return self.role


class CustomUser(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)



class Driver(models.Model):
    id = models.BigAutoField(primary_key=True)
    driver_name = models.CharField(unique=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'driver'


class Order(models.Model):
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    grade = models.CharField()
    quantity = models.FloatField()
    from_field = models.CharField(db_column='from')  # Field renamed because it was a Python reserved word.
    to = models.CharField()
    order_id = models.CharField()
    party_name = models.CharField()
    advance = models.CharField()
    loading = models.IntegerField(blank=True, null=True)
    unloading = models.IntegerField(blank=True, null=True)
    rto_pcl = models.IntegerField(blank=True, null=True)
    toll_gate = models.IntegerField(blank=True, null=True)
    total_expenses = models.IntegerField(blank=True, null=True)
    freight = models.IntegerField(blank=True, null=True)
    freight_amount = models.IntegerField(blank=True, null=True)
    driver_freight = models.IntegerField(blank=True, null=True)
    driver_amount = models.IntegerField(blank=True, null=True)
    order_submit_status = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    gst = models.BooleanField(default=False)
    gst_amount = models.FloatField(default=0)

    class Meta:
        db_table = 'order'


class OrderToTripMapping(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    order_id = models.TextField()
    trip_id = models.TextField()
    id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'order_to_trip_mapping'


class Trip(models.Model):
    trip_date = models.DateTimeField()
    diesel = models.FloatField(blank=True, null=True)
    trip_type = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    vehicle_id = models.CharField()
    updated_at = models.DateTimeField(auto_now=True)
    reading = models.IntegerField(blank=True, null=True)
    diesel_amount = models.FloatField(blank=True, null=True)
    ad_blue = models.FloatField(blank=True, null=True)
    kilometers = models.IntegerField(blank=True, null=True)
    no_of_trips = models.SmallIntegerField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    owner_name = models.CharField()
    mileage = models.FloatField(blank=True, null=True)
    submit_status = models.BooleanField(default=False)
    balance_amount = models.FloatField(blank=True, null=True)
    diesel_per_litre = models.FloatField(blank=True, null=True)
    total_expenses = models.FloatField(default=0)
    balance_with_gst = models.FloatField(default=0)

    class Meta:
        db_table = 'trip'


class Vehicle(models.Model):
    registration_number = models.CharField(primary_key=True, max_length=15, unique=True)  # The composite primary key (registration_number, id) found, that is not supported. The first column is selected.
    company = models.CharField(blank=False, null=False)
    chassis_number = models.CharField(blank=True, null=True)
    insurance = models.DateField(blank=True, null=True)
    fc = models.DateField(blank=True, null=True)
    status = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    driver_name = models.CharField(blank=True, null=True)
    rc = models.DateField(blank=True, null=True, db_comment='RC expire date')
    next_service_km_due = models.IntegerField(blank=False, default=0, db_comment='How many kilometers are remaining for next service due?')
    emis_tenure = models.IntegerField(blank=False, default=0, db_comment="Total No. of Months EMI is taken for")

    class Meta:
        db_table = 'vehicle'
        # unique_together = (('registration_number', 'id'),)


class Maintenance(models.Model):
    id = models.BigAutoField(primary_key=True)
    vehicle_id = models.ForeignKey('Vehicle', models.DO_NOTHING)
    maintenance_date = models.DateField(blank=False, null=False, db_comment='Maintenance activity registered date')
    maintenance_name = models.CharField(blank=False, null=False)
    charges = models.FloatField(blank=False, null=False)

    class Meta:
        db_table = 'maintenance'

class Emi(models.Model):
    DROPDOWN_CHOICES = [
        ('truck', 'truck'),
        ('loan', 'loan')
    ]
    id = models.BigAutoField(primary_key=True)
    vehicle_id = models.ForeignKey('Vehicle', models.DO_NOTHING)
    emi_date = models.DateField(blank=False, null=False, db_comment='EMI paid date or EMI submitted date')
    emi_type = models.CharField(
        max_length=5,
        choices=DROPDOWN_CHOICES,
        default='truck',
        verbose_name='EMI type'
    )
    emi_amount = models.FloatField(blank=False, null=False)

    class Meta:
        db_table = 'emi'

