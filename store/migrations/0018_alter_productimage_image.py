# Generated by Django 5.2.1 on 2025-05-31 13:11

import store.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='store/images', validators=[store.validators.validate_file_size]),
        ),
    ]
