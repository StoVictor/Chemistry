# Generated by Django 2.0 on 2018-03-18 13:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20180318_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='hard',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)]),
        ),
        migrations.AlterField(
            model_name='article',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 18, 14, 10, 43, 287823), verbose_name='date published'),
        ),
    ]