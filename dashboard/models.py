# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Comments(models.Model):
    order_id = models.IntegerField()
    text = models.TextField(blank=True, null=True, default='')

    class Meta:
        app_label = 'dashboard'

class Bids(models.Model):
    id = models.BigAutoField(primary_key=True)
    executor_id = models.IntegerField(blank=True, null=True)
    cargo_weight = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=4)
    status = models.IntegerField()
    order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    executor_legal_entity = models.ForeignKey('LegalEntities', models.DO_NOTHING, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vat_rate = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bids'
        app_label = 'default'

class LegalEntities(models.Model):
    id = models.BigAutoField(primary_key=True)
    inn = models.CharField(max_length=100, blank=True, null=True)
    #user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    organization_name = models.CharField(max_length=100, blank=True, null=True)
    tax_type = models.IntegerField()
    company_id = models.IntegerField(blank=True, null=True)
    color = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()
    create_power_of_attorney = models.BooleanField(blank=True, null=True)
    log_loading_start = models.BooleanField()
    role = models.IntegerField()
    auction_auto_renewal = models.BooleanField(blank=True, null=True)
    do_not_edit_my_orders = models.BooleanField(blank=True, null=True)
    calibrated = models.BooleanField()
    integration_1c = models.BooleanField()
    auction_settings = models.TextField()  # This field type is a guess.
    roles = models.TextField()  # This field type is a guess.
    organization_type = models.CharField(max_length=100, blank=True, null=True)
    trucker_lite = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'legal_entities'
        app_label = 'default'



class Orders(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    sender_id = models.IntegerField(blank=True, null=True)
    recipient_id = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sender_address = models.CharField(max_length=100, blank=True, null=True)
    recipient_address = models.CharField(max_length=100, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    cargo_weight = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    customer_id = models.IntegerField(blank=True, null=True)
    sender_name = models.CharField(max_length=100, blank=True, null=True)
    sender_phone = models.CharField(max_length=100, blank=True, null=True)
    recipient_name = models.CharField(max_length=100, blank=True, null=True)
    recipient_phone = models.CharField(max_length=100, blank=True, null=True)
    distance = models.FloatField()
    bid_rate = models.DecimalField(max_digits=12, decimal_places=2)
    sender_lat = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sender_lng = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    recipient_lat = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    recipient_lng = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    date_from = models.DateTimeField(blank=True, null=True)
    date_to = models.DateTimeField(blank=True, null=True)
    auction_close_date = models.DateTimeField(blank=True, null=True)
    date_delivery = models.DateTimeField(blank=True, null=True)
    customer_rate = models.DecimalField(max_digits=12, decimal_places=2)
    sender_country_name = models.CharField(max_length=100, blank=True, null=True)
    sender_region_id = models.IntegerField(blank=True, null=True)
    sender_sub_region_name = models.CharField(max_length=100, blank=True, null=True)
    sender_locality_name = models.CharField(max_length=100, blank=True, null=True)
    recipient_country_name = models.CharField(max_length=100, blank=True, null=True)
    recipient_region_id = models.IntegerField(blank=True, null=True)
    recipient_sub_region_name = models.CharField(max_length=100, blank=True, null=True)
    recipient_locality_name = models.CharField(max_length=100, blank=True, null=True)
    units = models.IntegerField()
    recipient_thoroughfare_name = models.CharField(max_length=100, blank=True, null=True)
    recipient_premise_number = models.CharField(max_length=100, blank=True, null=True)
    sender_thoroughfare_name = models.CharField(max_length=100, blank=True, null=True)
    sender_premise_number = models.CharField(max_length=100, blank=True, null=True)
    sender_dependent_locality_name = models.CharField(max_length=100, blank=True, null=True)
    recipient_dependent_locality_name = models.CharField(max_length=100, blank=True, null=True)
    rate_without_distance = models.BooleanField()
    weight_accounting_metering = models.IntegerField()
    sender_coords = models.TextField(blank=True, null=True)  # This field type is a guess.
    recipient_coords = models.TextField(blank=True, null=True)  # This field type is a guess.
    customer_legal_entity = models.ForeignKey(LegalEntities, models.DO_NOTHING, blank=True, null=True)
    cargo_volume = models.FloatField(blank=True, null=True)
    consolidated_cargo = models.BooleanField(blank=True, null=True)
    bid_total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    loading_by_executor = models.BooleanField(blank=True, null=True)
 #   order_group = models.ForeignKey(OrderGroups, models.DO_NOTHING, blank=True, null=True)
    payer_id = models.BigIntegerField(blank=True, null=True)
    show_description = models.BooleanField(blank=True, null=True)
    vat_rate = models.IntegerField(blank=True, null=True)
    vehicle_kinds = models.TextField(blank=True, null=True)  # This field type is a guess.
    cargo_kind = models.CharField(max_length=100, blank=True, null=True)
    agent_id = models.BigIntegerField(blank=True, null=True)
    recommended_rate = models.FloatField(blank=True, null=True)
 #   template = models.ForeignKey(OrderTemplates, models.DO_NOTHING, blank=True, null=True)
    commission_percent = models.FloatField(blank=True, null=True)
    is_trader = models.BooleanField(blank=True, null=True)
    customer_distance = models.FloatField()
    auction_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'
        app_label = 'default'


class Runs(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Orders, models.DO_NOTHING, blank=True, null=True)
    loaded = models.FloatField(blank=True, null=True)
    unloaded = models.FloatField(blank=True, null=True)
    status = models.IntegerField()
    loading_date = models.DateTimeField(blank=True, null=True)
    unloading_date = models.DateTimeField(blank=True, null=True)
 #   vehicle = models.ForeignKey('Vehicles', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    executor_id = models.IntegerField(blank=True, null=True)
    bid = models.ForeignKey(Bids, models.DO_NOTHING, blank=True, null=True)
    driver_id = models.IntegerField(blank=True, null=True)
    documents_received = models.BooleanField()
    cargo_weight = models.FloatField(blank=True, null=True)
    invoice_photo = models.CharField(max_length=100, blank=True, null=True)
    invoice_back_photo = models.CharField(max_length=100, blank=True, null=True)
    loading_lat = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    loading_lng = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    unloading_lat = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    unloading_lng = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    register_id = models.BigIntegerField(blank=True, null=True)
    consignment_note = models.CharField(max_length=100, blank=True, null=True)
    consignment_note_source = models.IntegerField(blank=True, null=True)
    executor_legal_entity = models.ForeignKey(LegalEntities, models.DO_NOTHING, blank=True, null=True)
    loading_start = models.DateTimeField(blank=True, null=True)
    unloading_start = models.DateTimeField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    trn_photo = models.CharField(max_length=100, blank=True, null=True)
    trn_back_photo = models.CharField(max_length=100, blank=True, null=True)
    invoice_created_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'runs'
        app_label = 'default'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=100)
    encrypted_password = models.CharField(max_length=100)
    reset_password_token = models.CharField(unique=True, max_length=100, blank=True, null=True)
    reset_password_sent_at = models.DateTimeField(blank=True, null=True)
    remember_created_at = models.DateTimeField(blank=True, null=True)
    sign_in_count = models.IntegerField()
    current_sign_in_at = models.DateTimeField(blank=True, null=True)
    last_sign_in_at = models.DateTimeField(blank=True, null=True)
    current_sign_in_ip = models.GenericIPAddressField(blank=True, null=True)
    last_sign_in_ip = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    full_name = models.CharField(max_length=100, blank=True, null=True)
    confirmation_token = models.CharField(unique=True, max_length=100, blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    confirmation_sent_at = models.DateTimeField(blank=True, null=True)
    unconfirmed_email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    default_vehicle_id = models.IntegerField(blank=True, null=True)
    current_run_id = models.IntegerField(blank=True, null=True)
    passport_info = models.CharField(max_length=100, blank=True, null=True)
    passport_photo = models.CharField(max_length=100, blank=True, null=True)
    last_notify_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField()
    promo_code = models.CharField(max_length=100, blank=True, null=True)
    failed_attempts = models.IntegerField()
    locked_at = models.DateTimeField(blank=True, null=True)
    phone_pin = models.IntegerField(blank=True, null=True)
    email_notice = models.BooleanField(blank=True, null=True)
    push_notice = models.BooleanField(blank=True, null=True)
    sms_notice = models.BooleanField(blank=True, null=True)
    websocket_notice = models.BooleanField(blank=True, null=True)
    guid_1c = models.CharField(max_length=100, blank=True, null=True)
    hide_other_regions = models.BooleanField(blank=True, null=True)
    notifications_settings = models.TextField(blank=True, null=True)  # This field type is a guess.
    roles = models.TextField(blank=True, null=True)  # This field type is a guess.
    company_id = models.IntegerField(blank=True, null=True)
    passport_series = models.CharField(max_length=100, blank=True, null=True)
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_date_of_issue = models.DateField(blank=True, null=True)
    passport_issued_by = models.CharField(max_length=100, blank=True, null=True)
    last_login_version = models.TextField(blank=True, null=True)  # This field type is a guess.
    default_legal_entity = models.ForeignKey('LegalEntities', models.DO_NOTHING, blank=True, null=True)
    recive_notifications_from_all_orders = models.BooleanField()
    free_at = models.DateTimeField(blank=True, null=True)
    vesava_check = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'users'
        app_label = 'default'
