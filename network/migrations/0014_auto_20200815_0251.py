# Generated by Django 3.0.8 on 2020-08-15 02:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0013_auto_20200808_2047'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-id']},
        ),
    ]
