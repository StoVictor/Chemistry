# Generated by Django 2.0 on 2018-04-01 15:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_auto_20180327_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='scientist',
            name='tags',
            field=models.ManyToManyField(to='articles.Tag'),
        ),
        migrations.AlterField(
            model_name='article',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 1, 17, 20, 50, 871211), verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='scientist',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 1, 17, 20, 50, 877216), verbose_name='date published'),
        ),
    ]
