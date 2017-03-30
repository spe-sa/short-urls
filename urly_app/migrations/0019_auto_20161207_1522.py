# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0018_auto_20161206_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='short_code',
            field=models.SlugField(max_length=18, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='testing_date',
            field=models.DateTimeField(default=None, null=True, verbose_name=b'Timestamp if Testing', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='link',
            unique_together=set([('short_base', 'short_code')]),
        ),
    ]
