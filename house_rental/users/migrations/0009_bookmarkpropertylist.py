# Generated by Django 3.1.1 on 2020-09-14 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200913_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookMarkPropertyList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmarked_properties', models.ManyToManyField(to='users.Property')),
                ('list_owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.tenant')),
            ],
        ),
    ]
