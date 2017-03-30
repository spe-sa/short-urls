# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0004_auto_20161026_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='requires_login',
            field=models.NullBooleanField(),
        ),
    ]
