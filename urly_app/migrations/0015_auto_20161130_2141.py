# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0014_auto_20161102_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='short_base',
            field=models.URLField(default=b'http://www.spe.org/go/', max_length=27, choices=[(b'http://go.spe.org/', b'GO.spe.org'), (b'http://www.spe.org/go/', b'SPE.org/go'), (b'http://www.iptcnet.org/go/', b'IPTCnet.org/go'), (b'http://www.otcnet.org/go/', b'OTCnet.org/go'), (b'http://www.otcbrasil.org/go/', b'OTCBrasil.org/go'), (b'http://www.otcasia.org/go/', b'OTCAsia.org/go'), (b'http://go.otcnet.org/', b'GO.OTCnet.org'), (b'http://go.otcbrasil.org/', b'GO.OTCBrasil.org'), (b'http://go.otcasia.org/', b'GO.OTCAsia.org'), (b'http://2s.pe/', b'2s.pe'), (b'http://4s.pe/', b'4s.pe')]),
        ),
    ]
