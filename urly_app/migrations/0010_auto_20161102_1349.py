# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0009_auto_20161028_1919'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='canonical',
            new_name='canonical_url',
        ),
        migrations.RenameField(
            model_name='link',
            old_name='tracking',
            new_name='tracking_string',
        ),
        migrations.RemoveField(
            model_name='link',
            name='track_server_side',
        ),
        migrations.AddField(
            model_name='link',
            name='tracking_type',
            field=models.CharField(default=b'c', max_length=1, choices=[(b's', b'Server-side'), (b'c', b'Client-side'), (b'n', b'No tracking')]),
        ),
    ]
