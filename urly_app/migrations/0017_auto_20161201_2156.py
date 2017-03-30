# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0016_auto_20161130_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='testing_date',
            field=models.DateTimeField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='short_base',
            field=models.URLField(default=b'http://www.spe.org/go/', max_length=28, choices=[(b'http://2s.pe/', b'2s.pe'), (b'http://4s.pe/', b'4s.pe'), (b'http://go.spe.org/', b'GO.spe.org'), (b'http://www.spe.org/go/', b'www.SPE.org/go'), (b'http://go.iptcnet.org/', b'GO.IPTCnet.org'), (b'http://www.iptcnet.org/go/', b'www.IPTCnet.org/go'), (b'http://go.otcnet.org/', b'GO.OTCnet.org'), (b'http://www.otcnet.org/go/', b'www.OTCnet.org/go'), (b'http://go.otcbrasil.org/', b'GO.OTCBrasil.org'), (b'http://www.otcbrasil.org/go/', b'www.OTCBrasil.org/go'), (b'http://go.otcasia.org/', b'GO.OTCAsia.org'), (b'http://www.otcasia.org/go/', b'www.OTCAsia.org/go')]),
        ),
    ]
