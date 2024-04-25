# Generated by Django 3.2.20 on 2024-04-25 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personnel_database', '0005_pangkat_tipe'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffingStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dsp', models.IntegerField()),
                ('rill', models.IntegerField()),
                ('pangkat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personnel_database.pangkat')),
                ('subsatker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personnel_database.subsatker')),
            ],
        ),
    ]