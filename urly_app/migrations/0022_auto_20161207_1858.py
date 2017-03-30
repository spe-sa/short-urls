# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0021_auto_20161207_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='accounting_code',
            field=models.CharField(help_text=b'Optional: the accounting code to associate with this short URL, for time and expenses, e.g., EZLabor code', max_length=6, blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='canonical_url',
            field=models.URLField(help_text=b'Please provide the standard (canonical) version of your long URL', verbose_name=b'Canonical URL'),
        ),
        migrations.AlterField(
            model_name='link',
            name='hit_count',
            field=models.IntegerField(default=0, help_text=b'How many times this short URL has been used', editable=False),
        ),
        migrations.AlterField(
            model_name='link',
            name='pub_date',
            field=models.DateTimeField(help_text=b'When this short URL was (last) published', verbose_name=b'Published', auto_now=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='pub_user',
            field=models.CharField(help_text=b'Who (last) published this short URL', max_length=90, verbose_name=b'Published By', blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='purpose',
            field=models.CharField(help_text=b'Please specify the reason you are creating this short URL', max_length=252, blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='short_base',
            field=models.URLField(default=b'http://www.spe.org/go/', help_text=b'Please select which prefix to use for your short URL', max_length=28, db_index=True, choices=[(b'http://2s.pe/', b'2s.pe'), (b'http://4s.pe/', b'4s.pe'), (b'http://go.spe.org/', b'GO.spe.org'), (b'http://www.spe.org/go/', b'www.SPE.org/go'), (b'http://go.iptcnet.org/', b'GO.IPTCnet.org'), (b'http://www.iptcnet.org/go/', b'www.IPTCnet.org/go'), (b'http://go.otcnet.org/', b'GO.OTCnet.org'), (b'http://www.otcnet.org/go/', b'www.OTCnet.org/go'), (b'http://go.otcbrasil.org/', b'GO.OTCBrasil.org'), (b'http://www.otcbrasil.org/go/', b'www.OTCBrasil.org/go'), (b'http://go.otcasia.org/', b'GO.OTCAsia.org'), (b'http://www.otcasia.org/go/', b'www.OTCAsia.org/go')]),
        ),
        migrations.AlterField(
            model_name='link',
            name='short_code',
            field=models.SlugField(help_text=b'Please choose the suffix for your short URL', max_length=18),
        ),
        migrations.AlterField(
            model_name='link',
            name='short_url_hash',
            field=models.SlugField(max_length=96, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='testing_date',
            field=models.DateTimeField(default=None, help_text=b'Only put a date and time here if this short URL is for testing purposes', null=True, verbose_name=b'Timestamp if Testing', blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='tracking_type',
            field=models.CharField(default=b'c', help_text=b'Please select how to track the usage of your short URL', max_length=1, choices=[(b's', b'Server-side'), (b'c', b'Client-side'), (b'n', b'No tracking')]),
        ),
    ]
