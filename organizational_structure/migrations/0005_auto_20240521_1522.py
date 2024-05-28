# Generated by Django 3.2.20 on 2024-05-21 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizational_structure', '0004_auto_20240513_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='nodes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='organizational_structure.nodes'),
        ),
        migrations.AlterField(
            model_name='nodes',
            name='child',
            field=models.ManyToManyField(blank=True, related_name='child_list', to='organizational_structure.Nodes'),
        ),
        migrations.AlterField(
            model_name='nodes',
            name='child_offsets',
            field=models.ManyToManyField(blank=True, related_name='child_offsets_list', to='organizational_structure.Nodes'),
        ),
    ]