# Generated by Django 3.2.20 on 2024-04-24 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel_database', '0002_alter_userpersonil_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpersonil',
            name='bko',
            field=models.CharField(choices=[('Gasus masuk', 'GASUS_MASUK'), ('Gasum masuk', 'GASUM_MASUK')], default='Gasum masuk', max_length=12),
            preserve_default=False,
        ),
    ]
