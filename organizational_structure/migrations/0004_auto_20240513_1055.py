# Generated by Django 3.2.20 on 2024-05-13 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizational_structure', '0003_auto_20240513_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nodes',
            name='child',
            field=models.ManyToManyField(blank=True, null=True, related_name='child_list', to='organizational_structure.Nodes'),
        ),
        migrations.AlterField(
            model_name='nodes',
            name='child_offsets',
            field=models.ManyToManyField(blank=True, null=True, related_name='child_offsets_list', to='organizational_structure.Nodes'),
        ),
    ]
