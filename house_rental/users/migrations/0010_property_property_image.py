# Generated by Django 3.1.1 on 2020-10-13 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_bookmarkpropertylist'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='property_image',
            field=models.ImageField(blank=True, upload_to='property_images/'),
        ),
    ]
