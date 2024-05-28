# Generated by Django 3.2.20 on 2024-05-28 00:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel_database', '0008_alter_userpersonil_nrp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpersonil',
            name='nrp',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(99999999)]),
        ),
    ]