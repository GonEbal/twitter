# Generated by Django 3.0.8 on 2020-07-28 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_modified',
            field=models.DateTimeField(blank=True),
        ),
    ]
