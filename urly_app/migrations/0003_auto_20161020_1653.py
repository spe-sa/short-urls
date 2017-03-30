# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0002_auto_20161019_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='pub_user',
            field=models.CharField(max_length=90),
        ),
        migrations.AlterField(
            model_name='link',
            name='tracking',
            field=models.CharField(max_length=234),
        ),
    ]
