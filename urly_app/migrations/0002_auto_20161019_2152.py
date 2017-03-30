# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='fragment',
        ),
        migrations.AddField(
            model_name='link',
            name='short_base',
            field=models.URLField(default='http://www.spe.org/go/'),
            preserve_default=False,
        ),
    ]
