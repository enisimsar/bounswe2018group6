# Generated by Django 2.1.2 on 2018-10-10 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20181010_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='downvote_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='event',
            name='upvote_count',
            field=models.IntegerField(default=0),
        ),
    ]
