# Generated by Django 2.0 on 2018-03-18 13:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20180318_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 18, 14, 17, 1, 670692), verbose_name='date published'),
        ),
    ]