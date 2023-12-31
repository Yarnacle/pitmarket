# Generated by Django 4.1.1 on 2022-09-17 01:58

from django.db import migrations, models
import listings.validators


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0012_listing_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(blank=True, upload_to='uploads/', validators=[listings.validators.validate_file_size]),
        ),
    ]
