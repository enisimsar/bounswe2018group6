# Generated by Django 2.1.2 on 2019-01-06 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_annotation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Location'),
        ),
    ]
