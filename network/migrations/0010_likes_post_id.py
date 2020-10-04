# Generated by Django 3.0.8 on 2020-08-03 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='likes',
            name='post_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='post_id', to='network.Post'),
            preserve_default=False,
        ),
    ]
