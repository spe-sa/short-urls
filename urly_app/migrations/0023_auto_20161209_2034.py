# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0022_auto_20161207_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 9, 20, 34, 23, 743977, tzinfo=utc), help_text=b'When this campaign will end and this short URL will no longer be needed', verbose_name=b'End Date', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='link',
            name='hit_count',
            field=models.IntegerField(default=0, help_text=b'How many times this short URL has already been used', editable=False),
        ),
    ]
