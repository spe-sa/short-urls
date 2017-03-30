# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urly_app', '0005_link_requires_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url_prefix', models.URLField()),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('purpose', models.CharField(max_length=252, blank=True)),
            ],
        ),
    ]
