# Generated by Django 3.0.8 on 2020-07-28 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20200728_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_modified',
            field=models.DateTimeField(null=True),
        ),
    ]