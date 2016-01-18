# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20160118_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.FileField(null=True, upload_to=b'profile_pictures', blank=True),
        ),
    ]
