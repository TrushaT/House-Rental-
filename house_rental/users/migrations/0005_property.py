# Generated by Django 3.1.1 on 2020-09-13 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200913_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_size', models.CharField(choices=[('1 BHK', '1 BHK'), ('2 BHK', '2 BHK'), ('3 BHK', '3 BHK'), ('4 BHK', '4 BHK')], max_length=100)),
                ('monthly_rent', models.PositiveIntegerField()),
                ('area', models.CharField(choices=[('Borivali', 'Borivali'), ('Kandivali', 'Kandivali'), ('Malad', 'Malad'), ('Goregaon', 'Goregaon')], max_length=100)),
                ('address_line_1', models.CharField(max_length=30)),
                ('address_line_2', models.CharField(max_length=30)),
                ('property_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.owner')),
            ],
        ),
    ]
