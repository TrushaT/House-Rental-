# Generated by Django 3.1.1 on 2020-10-24 18:58

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_tenant_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]