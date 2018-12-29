# Generated by Django 2.1.2 on 2018-12-28 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20181209_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='share_status', to='api.Event')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sharestatus_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='sharestatus',
            unique_together={('owner', 'event')},
        ),
    ]
