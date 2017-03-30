# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0008_auto_20161028_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='tracking',
            field=models.CharField(max_length=252, blank=True),
        ),
    ]
