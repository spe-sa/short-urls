# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0011_auto_20161102_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='short_base',
            field=models.URLField(default=b'http://www.spe.org/go/', max_length=18, choices=[(b'http://www.spe.org/go/', b'SPE.org/go'), (b'http://go.spe.org/', b'GO.spe.org'), (b'http://2s.pe/', b'2S.PE'), (b'http://4s.pe/', b'4S.PE')]),
        ),
        migrations.DeleteModel(
            name='ShortBase',
        ),
    ]
