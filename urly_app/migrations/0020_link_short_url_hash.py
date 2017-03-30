# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0019_auto_20161207_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='short_url_hash',
            field=models.SlugField(max_length=96, blank=True),
        ),
    ]
