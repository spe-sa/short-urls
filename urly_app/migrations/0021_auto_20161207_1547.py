# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0020_link_short_url_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='short_code',
            field=models.SlugField(max_length=18),
        ),
        migrations.AlterField(
            model_name='link',
            name='short_url_hash',
            field=models.SlugField(max_length=96, serialize=False, primary_key=True),
        ),
    ]
