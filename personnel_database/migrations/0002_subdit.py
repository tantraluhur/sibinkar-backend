# Generated by Django 3.2.20 on 2024-04-05 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel_database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubDit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nama', models.CharField(max_length=120)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
