# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0017_auto_20161201_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='canonical_url',
            field=models.URLField(verbose_name=b'Canonical URL'),
        ),
        migrations.AlterField(
            model_name='link',
            name='pub_date',
            field=models.DateTimeField(auto_now=True, verbose_name=b'Published'),
        ),
        migrations.AlterField(
            model_name='link',
            name='pub_user',
            field=models.CharField(max_length=90, verbose_name=b'Published By', blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='testing_date',
            field=models.DateTimeField(default=None, null=True, verbose_name=b'Testing? Timestamp', blank=True),
        ),
    ]
