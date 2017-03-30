# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0003_auto_20161020_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='purpose',
            field=models.CharField(max_length=252, blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='short_base',
            field=models.URLField(default=b'http://www.spe.org/go/'),
        ),
        migrations.AlterField(
            model_name='link',
            name='tracking',
            field=models.CharField(max_length=252),
        ),
    ]
