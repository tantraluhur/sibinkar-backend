# Generated by Django 3.2.20 on 2024-05-07 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel_database', '0007_auto_20240507_0721'),
        ('staffing_status', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffingstatus',
            name='nama',
            field=models.CharField(default='name', max_length=120, unique=True),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='staffingstatus',
            name='pangkat',
        ),
        migrations.AddField(
            model_name='staffingstatus',
            name='pangkat',
            field=models.ManyToManyField(to='personnel_database.Pangkat'),
        ),
    ]
