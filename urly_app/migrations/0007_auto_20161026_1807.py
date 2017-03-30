# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0006_shortbase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shortbase',
            name='id',
        ),
        migrations.AlterField(
            model_name='link',
            name='short_base',
            field=models.ForeignKey(to='urly_app.ShortBase'),
        ),
        migrations.AlterField(
            model_name='shortbase',
            name='url_prefix',
            field=models.URLField(serialize=False, primary_key=True),
        ),
    ]
