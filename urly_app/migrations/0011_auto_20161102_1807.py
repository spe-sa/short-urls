# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0010_auto_20161102_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='accounting_code',
            field=models.CharField(max_length=6, blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='pub_user',
            field=models.CharField(max_length=90, blank=True),
        ),
    ]
