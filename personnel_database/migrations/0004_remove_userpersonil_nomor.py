# Generated by Django 3.2.20 on 2024-04-24 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personnel_database', '0003_userpersonil_bko'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpersonil',
            name='nomor',
        ),
    ]