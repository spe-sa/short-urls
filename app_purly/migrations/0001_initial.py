# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('short_base', models.URLField(default=b'http://www.spe.org/go/', help_text=b'Please select which prefix to use for your short URL', max_length=28, db_index=True, choices=[(b'http://2s.pe/', b'2s.pe'), (b'http://4s.pe/', b'4s.pe'), (b'http://go.spe.org/', b'GO.spe.org'), (b'http://www.spe.org/go/', b'www.SPE.org/go'), (b'http://go.iptcnet.org/', b'GO.IPTCnet.org'), (b'http://www.iptcnet.org/go/', b'www.IPTCnet.org/go'), (b'http://go.otcnet.org/', b'GO.OTCnet.org'), (b'http://www.otcnet.org/go/', b'www.OTCnet.org/go'), (b'http://go.otcbrasil.org/', b'GO.OTCBrasil.org'), (b'http://www.otcbrasil.org/go/', b'www.OTCBrasil.org/go'), (b'http://go.otcasia.org/', b'GO.OTCAsia.org'), (b'http://www.otcasia.org/go/', b'www.OTCAsia.org/go')])),
                ('short_code', models.SlugField(help_text=b'Please choose the suffix for your short URL', max_length=18)),
                ('short_url_hash', models.SlugField(max_length=96, serialize=False, editable=False, primary_key=True)),
                ('canonical_url', models.URLField(help_text=b'Please provide the standard (canonical) version of your long URL', verbose_name=b'Canonical URL')),
                ('accounting_code', models.CharField(help_text=b'Optional: the accounting code to associate with this short URL, for time and expenses, e.g., EZLabor code', max_length=18, blank=True)),
                ('tracking_string', models.CharField(max_length=252, blank=True)),
                ('tracking_type', models.CharField(default=b'c', help_text=b'Please select how to track the usage of your short URL', max_length=1, choices=[(b's', b'Server-side'), (b'c', b'Client-side'), (b'n', b'No tracking')])),
                ('pub_date', models.DateTimeField(help_text=b'When this short URL was (last) published', verbose_name=b'Published', auto_now=True)),
                ('pub_user', models.CharField(help_text=b'Who (last) published this short URL', max_length=90, verbose_name=b'Published By', blank=True)),
                ('purpose', models.CharField(help_text=b'Please specify the reason you are creating this short URL', max_length=252, blank=True)),
                ('end_date', models.DateTimeField(help_text=b'When this campaign will end and this short URL will no longer be needed', verbose_name=b'End Date', blank=True)),
                ('hit_count', models.IntegerField(default=0, help_text=b'How many times this short URL has already been used', editable=False)),
                ('testing_date', models.DateTimeField(default=None, help_text=b'Only put a date and time here if this short URL is for testing purposes', null=True, verbose_name=b'Timestamp if Testing', blank=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='link',
            unique_together=set([('short_base', 'short_code')]),
        ),
    ]
