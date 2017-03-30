# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0007_auto_20161026_1807'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='requires_login',
            new_name='track_server_side',
        ),
    ]
