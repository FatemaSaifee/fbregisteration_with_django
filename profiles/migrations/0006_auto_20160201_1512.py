# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20160118_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='father_name',
            field=models.CharField(max_length=55, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='hobbies',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
