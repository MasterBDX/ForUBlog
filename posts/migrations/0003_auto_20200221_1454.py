# Generated by Django 2.2.1 on 2020-02-21 14:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20200221_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='timestamp',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
    ]
